# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import absolute_import, print_function, unicode_literals

import atexit
import gc
try:
    # Python 3: mock part of standard library.
    from unittest import mock
except ImportError:
    # Python 2: use 3rd-party mock
    import mock
import os
import shutil
import sys
import tempfile
import threading
import unittest
import warnings

try:
    import ipykernel  # noqa: F401
except ImportError:
    ipykernel_available = False
else:
    ipykernel_available = True

if ipykernel_available:
    import ipykernel.iostream
    import ipykernel.ipkernel
    import ipykernel.kernelapp
    import ipykernel.zmqshell
    import IPython.utils.io
    import tornado.ioloop
    import zmq

    from envisage.plugins.ipython_kernel.internal_ipkernel import (
        InternalIPKernel)


@unittest.skipUnless(ipykernel_available,
                     "skipping tests that require the ipykernel package")
class TestInternalIPKernel(unittest.TestCase):
    def setUp(self):
        # Make sure that IPython-related files are written to a temporary
        # directory instead of the home directory.
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)

        self._old_ipythondir = os.environ.get("IPYTHONDIR")
        os.environ["IPYTHONDIR"] = tmpdir

    def tearDown(self):
        # Restore previous state of the IPYTHONDIR environment variable.
        old_ipythondir = self._old_ipythondir
        if old_ipythondir is None:
            del os.environ["IPYTHONDIR"]
        else:
            os.environ["IPYTHONDIR"] = old_ipythondir

    def test_lifecycle(self):
        kernel = InternalIPKernel()
        self.assertIsNone(kernel.ipkernel)

        kernel.init_ipkernel(gui_backend=None)
        self.assertIsNotNone(kernel.ipkernel)
        self.assertIsInstance(kernel.ipkernel, ipykernel.kernelapp.IPKernelApp)

        kernel.new_qt_console()
        kernel.new_qt_console()
        self.assertEqual(len(kernel.consoles), 2)

        kernel.shutdown()
        self.assertIsNone(kernel.ipkernel)
        self.assertEqual(len(kernel.consoles), 0)

    def test_initial_namespace(self):
        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
        kernel.init_ipkernel(gui_backend=None)
        self.assertIn('x', kernel.namespace)
        self.assertEqual(kernel.namespace['x'], 42.1)
        kernel.shutdown()

    def test_shutdown_restores_output_streams(self):
        original_stdin = sys.stdin
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        self.create_and_destroy_kernel()

        self.assertIs(sys.stdin, original_stdin)
        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)

    def test_shutdown_restores_sys_modules_main(self):
        original_sys_modules_main = sys.modules["__main__"]
        self.create_and_destroy_kernel()
        self.assertIs(sys.modules["__main__"], original_sys_modules_main)

    def test_shutdown_restores_displayhook_and_excepthook(self):
        original_displayhook = sys.displayhook
        original_excepthook = sys.excepthook

        self.create_and_destroy_kernel()

        self.assertIs(sys.displayhook, original_displayhook)
        self.assertIs(sys.excepthook, original_excepthook)

    def test_shutdown_restores_sys_path(self):
        original_sys_path = sys.path[:]

        self.create_and_destroy_kernel()

        self.assertEqual(sys.path, original_sys_path)

    def test_shutdown_closes_console_pipes(self):
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        console = kernel.new_qt_console()
        self.assertFalse(console.stdout.closed)
        self.assertFalse(console.stderr.closed)
        kernel.shutdown()
        self.assertTrue(console.stdout.closed)
        self.assertTrue(console.stderr.closed)

    def test_ipython_util_io_globals_restored(self):
        original_io_stdin = IPython.utils.io.stdin
        original_io_stdout = IPython.utils.io.stdout
        original_io_stderr = IPython.utils.io.stderr

        self.create_and_destroy_kernel()

        self.assertIs(IPython.utils.io.stdin, original_io_stdin)
        self.assertIs(IPython.utils.io.stdout, original_io_stdout)
        self.assertIs(IPython.utils.io.stderr, original_io_stderr)

    def test_ipython_util_io_globals_restored_if_they_dont_exist(self):
        # Regression test for enthought/envisage#218
        original_io_stdin = IPython.utils.io.stdin
        original_io_stdout = IPython.utils.io.stdout
        original_io_stderr = IPython.utils.io.stderr

        del IPython.utils.io.stdin
        del IPython.utils.io.stdout
        del IPython.utils.io.stderr

        try:
            self.create_and_destroy_kernel()
            self.assertFalse(hasattr(IPython.utils.io, "stdin"))
            self.assertFalse(hasattr(IPython.utils.io, "stdout"))
            self.assertFalse(hasattr(IPython.utils.io, "stderr"))
        finally:
            IPython.utils.io.stdin = original_io_stdin
            IPython.utils.io.stdout = original_io_stdout
            IPython.utils.io.stderr = original_io_stderr

    def test_io_pub_thread_stopped(self):
        self.create_and_destroy_kernel()
        io_pub_threads = self.objects_of_type(ipykernel.iostream.IOPubThread)
        for thread in io_pub_threads:
            self.assertFalse(thread.thread.is_alive())

    def test_no_threads_leaked(self):
        threads_before = threading.active_count()
        self.create_and_destroy_kernel()
        threads_after = threading.active_count()
        self.assertEqual(threads_before, threads_after)

    def test_no_new_atexit_handlers(self):
        # Caution: this is a rather fragile and indirect test. We want
        # to know that all cleanup has happened when shutting down the
        # kernel, with none of that cleanup deferred to atexit handlers.
        #
        # Since we have no direct way to get hold of the atexit handlers on
        # Python 3, we instead use the number of referents from the
        # atexit module as a proxy.
        #
        # If this test starts failing, try adding a warmup cycle. If the
        # first call to self.create_and_destroy_kernel adds new referents,
        # that's not a big deal. But if every call consistently adds new
        # referents, then there's something to be fixed.
        atexit_handlers_before = len(gc.get_referents(atexit))
        self.create_and_destroy_kernel()
        atexit_handlers_after = len(gc.get_referents(atexit))

        self.assertEqual(atexit_handlers_before, atexit_handlers_after)

    def test_zmq_sockets_closed(self):
        # Previously, tests were leaking file descriptors linked to
        # zmq.Socket objects. Check that all extant sockets are closed.
        self.create_and_destroy_kernel()
        sockets = self.objects_of_type(zmq.Socket)
        self.assertTrue(all(socket.closed for socket in sockets))

    def test_ipykernel_live_objects(self):
        # Check that all IPython-related objects have been cleaned up
        # as expected.

        self.create_and_destroy_kernel()

        # Remove anything kept alive by cycles. (There are too many cycles
        # to break them individually.)
        gc.collect()

        shells = self.objects_of_type(ipykernel.zmqshell.ZMQInteractiveShell)
        self.assertEqual(shells, [])

        kernels = self.objects_of_type(ipykernel.ipkernel.IPythonKernel)
        self.assertEqual(kernels, [])

        kernel_apps = self.objects_of_type(ipykernel.kernelapp.IPKernelApp)
        self.assertEqual(kernel_apps, [])

    def test_initialize_twice(self):
        # Trying to re-initialize an already initialized IPKernelApp can
        # happen right now as a result of refactoring, but eventually
        # it should be an error. For now, it's a warning.
        kernel = InternalIPKernel()
        self.assertIsNone(kernel.ipkernel)
        kernel.init_ipkernel(gui_backend=None)
        try:
            self.assertIsNotNone(kernel.ipkernel)
            ipkernel = kernel.ipkernel

            with warnings.catch_warnings(record=True) as warn_msgs:
                warnings.simplefilter("always", category=DeprecationWarning)
                kernel.init_ipkernel(gui_backend=None)

            # Check that the existing kernel has not been replaced.
            self.assertIs(ipkernel, kernel.ipkernel)
        finally:
            kernel.shutdown()

        # Check that we got the expected warning message.
        self.assertEqual(len(warn_msgs), 1)
        message = str(warn_msgs[0].message)
        self.assertIn("already been initialized", message)

    def test_init_ipkernel_with_explicit_gui_backend(self):
        loop = tornado.ioloop.IOLoop.current()

        # Kernel initialization adds an "enter_eventloop" call to the
        # ioloop event loop queue. Mock to avoid modifying the actual event
        # loop.
        with mock.patch.object(loop, "add_callback") as mock_add_callback:
            with warnings.catch_warnings(record=True) as warn_msgs:
                warnings.simplefilter("always", category=DeprecationWarning)

                # Use of gui_backend is deprecated.
                kernel = InternalIPKernel()
                kernel.init_ipkernel(gui_backend="qt4")
                kernel.shutdown()

        mock_add_callback.reset_mock()

        # Check that we got the expected warning message.
        matching_messages = [
            msg for msg in warn_msgs
            if "gui_backend argument is deprecated" in str(msg.message)
        ]
        self.assertEqual(len(matching_messages), 1)

    # Helper functions.

    def objects_of_type(self, type):
        """
        Find and return a list of all currently tracked instances of the
        given type.
        """
        return [
            obj for obj in gc.get_objects()
            if isinstance(obj, type)
        ]

    def create_and_destroy_kernel(self):
        """
        Set up a new kernel with two associated consoles, then shut everything
        down.
        """
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        kernel.new_qt_console()
        kernel.new_qt_console()
        kernel.shutdown()
