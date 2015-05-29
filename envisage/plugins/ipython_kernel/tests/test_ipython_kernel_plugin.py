import unittest

from IPython.kernel.zmq.kernelapp import IPKernelApp

from envisage.application import Application
from envisage.core_plugin import CorePlugin
from envisage.plugins.ipython_kernel.internal_ipkernel import InternalIPKernel
from envisage.plugins.ipython_kernel.ipython_kernel_plugin import (
    IPYTHON_KERNEL_PROTOCOL, IPythonKernelPlugin)


class TestIPythonKernelPlugin(unittest.TestCase):

    def tearDown(self):
        IPKernelApp.clear_instance()

    def test_kernel_service(self):
        # See that we can get the IPython kernel service when the plugin is
        # there.
        kernel_plugin = IPythonKernelPlugin()
        app = Application(plugins=[CorePlugin(), kernel_plugin], id='test')

        # Starting the app starts the kernel plugin. The IPython kernel
        # service should now be available.
        app.start()
        kernel = app.get_service(IPYTHON_KERNEL_PROTOCOL)
        self.assertIsNotNone(kernel)
        self.assertIsInstance(kernel, InternalIPKernel)

        # Initialize the kernel. Normally, the application does it when
        # it starts.
        kernel.init_ipkernel(gui_backend=None)

        # Stopping the application should shut the kernel down.
        app.stop()
        self.assertIsNone(kernel.ipkernel)
