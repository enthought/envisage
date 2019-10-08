# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An  IPython kernel plugin. """

import logging
import warnings

# Enthought library imports.
from envisage.api import (
    bind_extension_point, ExtensionPoint, Plugin, ServiceOffer)
from traits.api import Instance, List


IPYTHON_KERNEL_PROTOCOL = 'envisage.plugins.ipython_kernel.internal_ipkernel.InternalIPKernel'  # noqa
IPYTHON_NAMESPACE = 'ipython_plugin.namespace'


logger = logging.getLogger(__name__)


class IPythonKernelPlugin(Plugin):
    """ An IPython kernel plugin. """

    # Extension point IDs.
    SERVICE_OFFERS = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin unique identifier.
    id = 'envisage.plugins.ipython_kernel'

    # The plugin name (suitable for displaying to the user).
    name = 'IPython embedded kernel plugin'

    def stop(self):
        self._destroy_kernel()

    #### Extension points offered by this plugin ##############################

    kernel_namespace = ExtensionPoint(
        List, id=IPYTHON_NAMESPACE, desc="""

        Variables to add to the IPython kernel namespace.
        This is a list of tuples (name, value).

        """
    )

    #### Contributions to extension points made by this plugin ################

    service_offers = List(contributes_to=SERVICE_OFFERS)

    # Private traits and methods

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
        return kernel

    def _destroy_kernel(self):
        """
        Destroy any existing kernel.
        """
        if self._kernel is None:
            return

        logger.debug('Shutting down the embedded ipython kernel')
        self._kernel.shutdown()
        self._kernel = None

    def _service_offers_default(self):
        ipython_kernel_service_offer = ServiceOffer(
            protocol=IPYTHON_KERNEL_PROTOCOL,
            factory=self._create_kernel,
        )
        return [ipython_kernel_service_offer]
