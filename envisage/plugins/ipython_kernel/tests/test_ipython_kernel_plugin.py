# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
import unittest

from traits.api import List

from envisage._compat import STRING_BASE_CLASS
from envisage.api import Application, Plugin
from envisage.core_plugin import CorePlugin

# Skip these tests unless ipykernel is available.
try:
    import ipykernel  # noqa: F401
except ImportError:
    ipykernel_available = False
else:
    ipykernel_available = True

if ipykernel_available:
    from ipykernel.kernelapp import IPKernelApp

    from envisage.plugins.ipython_kernel.internal_ipkernel import (
        InternalIPKernel)
    from envisage.plugins.ipython_kernel.ipython_kernel_plugin import (
        IPYTHON_KERNEL_PROTOCOL, IPYTHON_NAMESPACE, IPythonKernelPlugin)


@unittest.skipUnless(ipykernel_available,
                     "skipping tests that require the ipykernel package")
class TestIPythonKernelPlugin(unittest.TestCase):

    def tearDown(self):
        IPKernelApp.clear_instance()

    def test_import_from_api(self):
        # Regression test for enthought/envisage#108
        from envisage.plugins.ipython_kernel.api import IPYTHON_KERNEL_PROTOCOL
        self.assertIsInstance(IPYTHON_KERNEL_PROTOCOL, STRING_BASE_CLASS)

    def test_kernel_service(self):
        # See that we can get the IPython kernel service when the plugin is
        # there.
        plugins = [CorePlugin(), IPythonKernelPlugin()]
        app = Application(plugins=plugins, id='test')

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

    def test_kernel_namespace_extension_point(self):
        class NamespacePlugin(Plugin):
            kernel_namespace = List(contributes_to=IPYTHON_NAMESPACE)

            def _kernel_namespace_default(self):
                return [('y', 'hi')]

        plugins = [CorePlugin(), IPythonKernelPlugin(), NamespacePlugin()]
        app = Application(plugins=plugins, id='test')

        app.start()
        try:
            kernel = app.get_service(IPYTHON_KERNEL_PROTOCOL)
            kernel.init_ipkernel(gui_backend=None)
            self.assertIn('y', kernel.namespace)
            self.assertEqual(kernel.namespace['y'], 'hi')
        finally:
            app.stop()
