import contextlib
import gc
import os
import shutil
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


@contextlib.contextmanager
def temp_filename(filename):
    tmpdir = tempfile.mkdtemp()
    try:
        yield os.path.join(tmpdir, filename)
    finally:
        shutil.rmtree(tmpdir)


@contextlib.contextmanager
def redirect_stdout_to(filename):
    """ Redirect stdout to a file, in a way that's immune to changes
    to Python's sys.stdout.

    Parameters
    ----------
    filename : str
        Path to filename to use for the redirected output.
    """
    with open(filename, 'w') as stream:
        stdout_fd = sys.__stdout__.fileno()
        old_stdout_fd = os.dup(stdout_fd)
        dest_fd = stream.fileno()
        os.dup2(dest_fd, stdout_fd)
        try:
            yield
        finally:
            sys.__stdout__.flush()
            os.dup2(old_stdout_fd, stdout_fd)
            os.close(old_stdout_fd)


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

    def test_shutdown_restores_displayhook_and_excepthook(self):
        original_displayhook = sys.displayhook
        original_excepthook = sys.excepthook

        self.create_and_destroy_kernel()

        self.assertIs(sys.displayhook, original_displayhook)
        self.assertIs(sys.excepthook, original_excepthook)

    def test_shutdown_closes_console_pipes(self):
        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
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

        # Sometimes once isn't enough ....
        # XXX Ideally, this wouldn't be necessary at all; see if we can fix.
        for _ in range(3):
            gc.collect()

        shells = self.objects_of_type(ipykernel.zmqshell.ZMQInteractiveShell)
        self.assertEqual(shells, [])

        kernels = self.objects_of_type(ipykernel.ipkernel.IPythonKernel)
        self.assertEqual(kernels, [])

        kernel_apps = self.objects_of_type(ipykernel.kernelapp.IPKernelApp)
        self.assertEqual(kernel_apps, [])

    def test_ctrl_c_message_suppressed(self):
        with temp_filename("captured_stdout.txt") as captured_stdout:
            with redirect_stdout_to(captured_stdout):
                kernel = InternalIPKernel()
                kernel.init_ipkernel(gui_backend=None)
                kernel.shutdown()

            with open(captured_stdout, "rb") as f:
                stdout = f.read().decode("utf-8")

        self.assertNotIn("Ctrl-C will not work", stdout)

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
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        kernel.new_qt_console()
        kernel.new_qt_console()
        kernel.shutdown()
