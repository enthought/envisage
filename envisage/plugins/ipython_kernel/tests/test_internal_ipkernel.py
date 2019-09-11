from __future__ import absolute_import, print_function, unicode_literals

import atexit
import contextlib
import gc
import logging
import os
import sys
import tempfile
import threading
import unittest

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
    import zmq

    from envisage.plugins.ipython_kernel.internal_ipkernel import (
        InternalIPKernel)


# Machinery for catching logged messages in tests (both for testing
# the existence and content of those messages, and for hiding the
# logger output during the test run).

class ListHandler(logging.Handler):
    """
    Simple logging handler that stores all records in a list.

    Used by catch_logs below.
    """
    def __init__(self):
        logging.Handler.__init__(self)
        self.records = []

    def emit(self, record):
        self.records.append(record)


@contextlib.contextmanager
def catch_logs(logger_name, level=logging.WARNING):
    """
    Temporarily redirect logs for the given logger to a list.

    Also allows temporarily changing the level of that logger.
    """
    logger = logging.getLogger(logger_name)
    handler = ListHandler()
    old_propagate = logger.propagate
    old_level = logger.level

    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(level)
    try:
        yield handler.records
    finally:
        logger.setLevel(old_level)
        logger.propagate = old_propagate
        logger.removeHandler(handler)


@contextlib.contextmanager
def capture_stream(stream, callback=None):
    """
    Context manager to capture output to a particular stream.

    Capture all output written to the given stream. If the optional
    callback is provided, call it with the captured output (which
    will be a bytestring) when exiting the with block.

    Parameters
    ----------
    stream : Python stream
        For example, sys.__stdout__.
    callback : callable
        Callable of a single argument.
    """
    stream_fd = stream.fileno()

    with tempfile.TemporaryFile() as new_stream:
        old_stream_fd = os.dup(stream_fd)
        stream.flush()
        os.dup2(new_stream.fileno(), stream_fd)
        try:
            yield
        finally:
            stream.flush()
            os.dup2(old_stream_fd, stream_fd)
            os.close(old_stream_fd)

        new_stream.flush()
        new_stream.seek(0)
        captured = new_stream.read()

    if callback is not None:
        callback(captured)


@unittest.skipUnless(ipykernel_available,
                     "skipping tests that require the ipykernel package")
class TestInternalIPKernel(unittest.TestCase):

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
        original_io_raw_print = IPython.utils.io.raw_print
        original_io_raw_print_err = IPython.utils.io.raw_print_err

        self.create_and_destroy_kernel()

        self.assertIs(IPython.utils.io.stdin, original_io_stdin)
        self.assertIs(IPython.utils.io.stdout, original_io_stdout)
        self.assertIs(IPython.utils.io.stderr, original_io_stderr)
        self.assertIs(IPython.utils.io.raw_print, original_io_raw_print)
        self.assertIs(
            IPython.utils.io.raw_print_err, original_io_raw_print_err)

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

    def test_ctrl_c_message_suppressed(self):
        captured = []
        with capture_stream(sys.__stdout__, callback=captured.append):
            self.create_and_destroy_kernel()

        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertNotIn("Ctrl-C will not work", captured_stdout)

    def test_ctrl_c_message_restored(self):
        original_ctrl_c_message = ipykernel.kernelapp._ctrl_c_message

        self.create_and_destroy_kernel()

        self.assertEqual(
            ipykernel.kernelapp._ctrl_c_message,
            original_ctrl_c_message,
        )

    def test_raw_print_logged(self):
        test_message = "norwegian blue"

        # Outside the context of the kernel, raw_print prints as expected.
        captured = []
        with capture_stream(sys.__stdout__, callback=captured.append):
            IPython.utils.io.raw_print(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

        # Again, with a running kernel.
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        captured = []
        log_catcher = catch_logs(
            "envisage.plugins.ipython_kernel", level=logging.INFO)

        try:
            with log_catcher as log_records:
                with capture_stream(sys.__stdout__, callback=captured.append):
                    IPython.utils.io.raw_print(test_message)
        finally:
            kernel.shutdown()

        # Check captured output (which should not contain the test message)
        # and the INFO-level log records (which should).
        messages = [
            record.getMessage() for record in log_records
            if record.levelno == logging.INFO
        ]
        test_message_found = any(
            test_message in message for message in messages)
        self.assertTrue(
            test_message_found,
            msg="raw_print messages were not found in the logs"
        )
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertNotIn(test_message, captured_stdout)

        # After shutdown, raw_print again prints to __stdout__.
        captured = []
        with capture_stream(sys.__stdout__, callback=captured.append):
            IPython.utils.io.raw_print(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

    def test_raw_print_err_logged(self):
        test_message = "your hovercraft is full of eels"

        # Outside the context of the kernel, raw_print_err prints as expected.
        captured = []
        with capture_stream(sys.__stderr__, callback=captured.append):
            IPython.utils.io.raw_print_err(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

        # Again, with a running kernel.
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        captured = []
        log_catcher = catch_logs(
            "envisage.plugins.ipython_kernel", level=logging.WARNING)

        try:
            with log_catcher as log_records:
                with capture_stream(sys.__stderr__, callback=captured.append):
                    IPython.utils.io.raw_print_err(test_message)
        finally:
            kernel.shutdown()

        # Check captured output (which should not contain the test message)
        # and the INFO-level log records (which should).
        messages = [
            record.getMessage() for record in log_records
            if record.levelno == logging.WARNING
        ]
        test_message_found = any(
            test_message in message for message in messages)
        self.assertTrue(
            test_message_found,
            msg="raw_print_err messages were not found in the logs"
        )
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertNotIn(test_message, captured_stdout)

        # After shutdown, raw_print_err again prints to __stderr__.
        captured = []
        with capture_stream(sys.__stderr__, callback=captured.append):
            IPython.utils.io.raw_print_err(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

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
        Set up a new kernel with two associate consoles, then shut everything
        down.
        """
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        kernel.new_qt_console()
        kernel.new_qt_console()
        kernel.shutdown()
