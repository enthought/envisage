# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" An IPython kernel plugin. """

import logging
import warnings

# Enthought library imports.
from envisage.api import (
    bind_extension_point, ExtensionPoint, Plugin, ServiceOffer)
from traits.api import Bool, Instance, List


# Extension point IDs.
SERVICE_OFFERS = 'envisage.service_offers'
IPYTHON_NAMESPACE = 'ipython_plugin.namespace'

# Protocol for the contributed service offer.
IPYTHON_KERNEL_PROTOCOL = 'envisage.plugins.ipython_kernel.internal_ipkernel.InternalIPKernel'  # noqa: E501

logger = logging.getLogger(__name__)


class IPythonKernelPlugin(Plugin):
    """ An IPython kernel plugin. """

    #: The plugin unique identifier.
    id = 'envisage.plugins.ipython_kernel'

    #: The plugin name (suitable for displaying to the user).
    name = 'IPython embedded kernel plugin'

    #: Extension point for objects contributed to the IPython kernel namespace.
    kernel_namespace = ExtensionPoint(
        List, id=IPYTHON_NAMESPACE, desc="""

        Variables to add to the IPython kernel namespace.
        This is a list of tuples (name, value).

        """
    )

    #: Service offers contributed by this plugin.
    service_offers = List(contributes_to=SERVICE_OFFERS)

    #: Whether to initialize the kernel when the service is created.
    #: The default is ``False```, for backwards compatibility. It will change
    #: to ``True`` in a future version of Envisage. External users wanting
    #: to use the future behaviour now should pass ``init_ipkernel=True``
    #: when creating the plugin.
    init_ipkernel = Bool(False)

    def stop(self):
        """ Stop the plugin. """
        self._destroy_kernel()

    # Private traits and methods

    #: The InternalIPKernel instance provided by the service.
    _kernel = Instance(IPYTHON_KERNEL_PROTOCOL)

    def _create_kernel(self):
        from .internal_ipkernel import InternalIPKernel

        # This shouldn't happen with a normal lifecycle, but add a warning
        # just in case.
        if self._kernel is not None:
            warnings.warn(
                "A kernel already exists. "
                "No new kernel will be created.",
                RuntimeWarning,
            )
            return

        logger.debug("Creating the embedded IPython kernel")
        kernel = self._kernel = InternalIPKernel()
        bind_extension_point(kernel, 'initial_namespace',
                             IPYTHON_NAMESPACE, self.application)
        if self.init_ipkernel:
            kernel.init_ipkernel()
        else:
            warnings.warn(
                (
                    "In the future, the IPython kernel will be initialized "
                    "automatically at creation time. To enable this "
                    "future behaviour now, create the plugin using "
                    "IPythonKernelPlugin(init_ipkernel=True)"
                ),
                DeprecationWarning,
            )

        return kernel

    def _destroy_kernel(self):
        """
        Destroy any existing kernel.
        """
        if self._kernel is None:
            return

        logger.debug("Shutting down the embedded IPython kernel")
        self._kernel.shutdown()
        self._kernel = None

    def _service_offers_default(self):
        ipython_kernel_service_offer = ServiceOffer(
            protocol=IPYTHON_KERNEL_PROTOCOL,
            factory=self._create_kernel,
        )
        return [ipython_kernel_service_offer]
