# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import contextlib
import os
try:
    # Python 3: mock available in std. lib.
    from unittest import mock
except ImportError:
    # Python 2: use 3rd party mock library
    import mock
import shutil
import tempfile
import unittest
import warnings

from traits.api import List

from envisage._compat import STRING_BASE_CLASS
from envisage.api import Application, Plugin
from envisage.core_plugin import CorePlugin
from envisage.tests.ets_config_patcher import ETSConfigPatcher

# Skip these tests unless ipykernel is available.
try:
    import ipykernel  # noqa: F401
except ImportError:
    ipykernel_available = False
else:
    ipykernel_available = True

if ipykernel_available:
    from envisage.plugins.ipython_kernel.internal_ipkernel import (
        InternalIPKernel)
    from envisage.plugins.ipython_kernel.ipython_kernel_plugin import (
        IPYTHON_KERNEL_PROTOCOL, IPYTHON_NAMESPACE, IPythonKernelPlugin)


@unittest.skipUnless(ipykernel_available,
                     "skipping tests that require the ipykernel package")
class TestIPythonKernelPlugin(unittest.TestCase):
    def setUp(self):
        ets_config_patcher = ETSConfigPatcher()
        ets_config_patcher.start()
        self.addCleanup(ets_config_patcher.stop)

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

    def test_import_from_api(self):
        # Regression test for enthought/envisage#108
        from envisage.plugins.ipython_kernel.api import IPYTHON_KERNEL_PROTOCOL
        self.assertIsInstance(IPYTHON_KERNEL_PROTOCOL, STRING_BASE_CLASS)

    def test_kernel_service(self):
        # See that we can get the IPython kernel service when the plugin is
        # there.
        with self.running_app() as app:
            kernel = app.get_service(IPYTHON_KERNEL_PROTOCOL)
            self.assertIsInstance(kernel, InternalIPKernel)
            self.assertIsNotNone(kernel.ipkernel)

        # After application stop, the InternalIPKernel object should
        # also have been shut down.
        self.assertIsNone(kernel.ipkernel)

    def test_kernel_namespace_extension_point(self):
        class NamespacePlugin(Plugin):
            kernel_namespace = List(contributes_to=IPYTHON_NAMESPACE)

            def _kernel_namespace_default(self):
                return [('y', 'hi')]

        plugins = [
            IPythonKernelPlugin(init_ipkernel=True),
            NamespacePlugin(),
        ]

        with self.running_app(plugins=plugins) as app:
            kernel = app.get_service(IPYTHON_KERNEL_PROTOCOL)
            self.assertIn('y', kernel.namespace)
            self.assertEqual(kernel.namespace['y'], 'hi')

    def test_get_service_twice(self):
        with self.running_app() as app:
            kernel1 = app.get_service(IPYTHON_KERNEL_PROTOCOL)
            kernel2 = app.get_service(IPYTHON_KERNEL_PROTOCOL)
            self.assertIs(kernel1, kernel2)

    def test_service_not_used(self):
        # If the service isn't used, no kernel should be created.
        from envisage.plugins.ipython_kernel import internal_ipkernel

        kernel_instances = []

        class TrackingInternalIPKernel(internal_ipkernel.InternalIPKernel):
            def __init__(self, *args, **kwargs):
                super(TrackingInternalIPKernel, self).__init__(*args, **kwargs)
                kernel_instances.append(self)

        patcher = mock.patch.object(
            internal_ipkernel,
            "InternalIPKernel",
            TrackingInternalIPKernel,
        )

        with patcher:
            kernel_plugin = IPythonKernelPlugin(init_ipkernel=True)
            with self.running_app(plugins=[kernel_plugin]):
                pass

        self.assertEqual(kernel_instances, [])

    def test_service_used(self):
        # This is a complement to the test_service_not_used test. It's mostly
        # here as a double check on the somewhat messy test machinery used in
        # test_service_not_used: if the assumptions (e.g., on the location that
        # InternalIPKernel is imported from) in test_service_not_used break,
        # then this test will likely break too.

        from envisage.plugins.ipython_kernel import internal_ipkernel

        kernel_instances = []

        class TrackingInternalIPKernel(internal_ipkernel.InternalIPKernel):
            def __init__(self, *args, **kwargs):
                super(TrackingInternalIPKernel, self).__init__(*args, **kwargs)
                kernel_instances.append(self)

        patcher = mock.patch.object(
            internal_ipkernel,
            "InternalIPKernel",
            TrackingInternalIPKernel,
        )

        with patcher:
            kernel_plugin = IPythonKernelPlugin(init_ipkernel=True)
            with self.running_app(plugins=[kernel_plugin]) as app:
                app.get_service(IPYTHON_KERNEL_PROTOCOL)

        self.assertEqual(len(kernel_instances), 1)

    def test_no_init(self):
        # Testing deprecated behaviour where the kernel is not initialized.
        plugins = [IPythonKernelPlugin()]

        with self.running_app(plugins=plugins) as app:
            with warnings.catch_warnings(record=True) as warn_msgs:
                warnings.simplefilter("always", category=DeprecationWarning)
                app.get_service(IPYTHON_KERNEL_PROTOCOL)

        matching_messages = [
            msg for msg in warn_msgs
            if isinstance(msg.message, DeprecationWarning)
            if "kernel will be initialized" in str(msg.message)
        ]
        self.assertEqual(len(matching_messages), 1)

    @contextlib.contextmanager
    def running_app(self, plugins=None):
        """
        Returns a context manager that provides a running application.

        Parameters
        ----------
        plugins : list of Plugin, optional
            Plugins to use in the application, other than the CorePlugin
            (which is always included). If not given, an IPythonKernelPlugin
            is instantiated and used.
        """
        if plugins is None:
            plugins = [IPythonKernelPlugin(init_ipkernel=True)]

        app = Application(plugins=[CorePlugin()] + plugins, id='test')
        app.start()
        try:
            yield app
        finally:
            app.stop()
