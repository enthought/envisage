import gc
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
