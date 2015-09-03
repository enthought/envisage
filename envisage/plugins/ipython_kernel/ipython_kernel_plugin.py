""" An  IPython kernel plugin. """

import logging

# Enthought library imports.
from envisage.ui.tasks.api import TaskExtension
from envisage.api import (bind_extension_point, ExtensionPoint, Plugin,
    ServiceOffer)
from traits.api import Instance, List
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

    #### Extension points offered by this plugin ##############################

    kernel_namespace = ExtensionPoint(
        List, id=IPYTHON_NAMESPACE, desc="""

        Variables to add to the IPython kernel namespace.
        This is a list of tuples (name, value).

        """
    )

    #### Contributions to extension points made by this plugin ################

    kernel = Instance(
        'envisage.plugins.ipython_kernel.internal_ipkernel.InternalIPKernel')

    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):

        ipython_kernel_service_offer = ServiceOffer(
            protocol=IPYTHON_KERNEL_PROTOCOL,
            factory=self._create_kernel,
        )
        return [ipython_kernel_service_offer]

    def _create_kernel(self):
        return self.kernel

    contributed_task_extensions = List(contributes_to=TASK_EXTENSIONS)

    #### Trait initializers ###################################################

    def _kernel_default(self):
        from .internal_ipkernel import InternalIPKernel
        kernel = InternalIPKernel()
        bind_extension_point(kernel, 'initial_namespace',
                     IPYTHON_NAMESPACE, self.application)
        return kernel

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