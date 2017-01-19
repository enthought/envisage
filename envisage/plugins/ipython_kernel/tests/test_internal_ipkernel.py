import unittest

try:
    import IPython  # noqa
except ImportError:
    from nose.plugins.skip import SkipTest
    raise SkipTest('IPython not available')

from ipykernel.kernelapp import IPKernelApp
from envisage.plugins.ipython_kernel.internal_ipkernel import InternalIPKernel


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
