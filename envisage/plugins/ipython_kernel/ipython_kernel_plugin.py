""" An  IPython kernel plugin. """

import logging

# Enthought library imports.
from envisage.ui.tasks.api import TaskExtension
from envisage.api import Plugin, ServiceOffer
from traits.api import List
from pyface.tasks.action.api import SGroup, SchemaAddition

IPYTHON_KERNEL_PROTOCOL = 'envisage.plugins.ipython_kernel.ipython_kernel_plugin.IPythonKernelPlugin'  # noqa
IPYTHON_NAMESPACE = 'ipython_plugin.namespace'
TASK_EXTENSIONS = 'envisage.ui.tasks.task_extensions'


logger = logging.getLogger(__name__)


class IPythonKernelPlugin(Plugin):
    """ An IPython kernel plugin. """

    # Extension point IDs.
    SERVICE_OFFERS = 'envisage.service_offers'
    PREFERENCES = 'envisage.preferences'

    #### 'IPlugin' interface ##################################################

    # The plugin unique identifier.
    id = 'envisage.plugins.ipython_kernel'

    # The plugin name (suitable for displaying to the user).
    name = 'IPython embedded kernel plugin'

    def stop(self):
        logger.info('Shutting down the embedded ipython kernel')
        self.kernel.shutdown()

    #### Contributions to extension points made by this plugin ################

    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):

        ipython_kernel_service_offer = ServiceOffer(
            protocol=IPYTHON_KERNEL_PROTOCOL,
            factory=self._create_kernel,
        )
        return [ipython_kernel_service_offer]

    def _create_kernel(self):

        from .internal_ipkernel import InternalIPKernel

        kernel = self.kernel = InternalIPKernel()

        return kernel

    contributed_task_extensions = List(contributes_to=TASK_EXTENSIONS)

    #### Trait initializers ###################################################

    def _contributed_task_extensions_default(self):

        from .actions import StartQtConsoleAction

        def menu_factory():
            return SGroup(
                StartQtConsoleAction(kernel=self.kernel),
                id='ipython'
            )

        return [
            TaskExtension(
                actions=[
                    SchemaAddition(
                        path='MenuBar/View',
                        factory=menu_factory,
                        id='IPythonSchema',),
                ]
            )
        ]
