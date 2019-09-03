import contextlib
import gc
import os
import shutil
import sys
import tempfile
import unittest

try:
    import ipykernel  # noqa: F401
except ImportError:
    ipykernel_available = False
else:
    ipykernel_available = True


if ipykernel_available:
    from ipykernel.iostream import IOPubThread
    from ipykernel.kernelapp import IPKernelApp

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
    """ Redirect stdout output from C libraries to a file.

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

    def tearDown(self):
        IPKernelApp.clear_instance()

    def test_lifecycle(self):
        kernel = InternalIPKernel()
        self.assertIsNone(kernel.ipkernel)

        kernel.init_ipkernel(gui_backend=None)
        self.assertIsNotNone(kernel.ipkernel)
        self.assertIsInstance(kernel.ipkernel, IPKernelApp)

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
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
        kernel.init_ipkernel(gui_backend=None)
        kernel.shutdown()

        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)

    def test_shutdown_closes_console_pipes(self):
        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
        kernel.init_ipkernel(gui_backend=None)
        console = kernel.new_qt_console()
        self.assertFalse(console.stdout.closed)
        self.assertFalse(console.stderr.closed)
        kernel.shutdown()
        self.assertTrue(console.stdout.closed)
        self.assertTrue(console.stderr.closed)

    def test_io_pub_thread_stopped(self):
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        kernel.new_qt_console()
        kernel.new_qt_console()
        kernel.shutdown()

        io_pub_threads = [
            obj for obj in gc.get_objects()
            if isinstance(obj, IOPubThread)
        ]

        for thread in io_pub_threads:
            self.assertFalse(thread.thread.is_alive())

    def test_ctrl_c_message_suppressed(self):
        with temp_filename("captured_stdout.txt") as captured_stdout:
            with redirect_stdout_to(captured_stdout):
                kernel = InternalIPKernel()
                kernel.init_ipkernel(gui_backend=None)
                kernel.shutdown()

            with open(captured_stdout, "rb") as f:
                stdout = f.read().decode("utf-8")

        self.assertNotIn("Ctrl-C will not work", stdout)
