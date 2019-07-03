# Standard library imports.
import logging

# Enthought library imports.
from envisage.api import Plugin
from envisage.core_plugin import CorePlugin
from envisage.plugins.ipython_kernel.ipython_kernel_ui_plugin import (
    IPythonKernelUIPlugin)
from envisage.plugins.ipython_kernel.api import (
    IPythonKernelPlugin, IPYTHON_KERNEL_PROTOCOL)
from envisage.ui.tasks.api import TasksApplication, TaskFactory
from envisage.ui.tasks.tasks_plugin import TasksPlugin
from pyface.qt import QtCore
from pyface.tasks.api import TaskWindowLayout
from pyface.util.guisupport import get_app_qt4
from traits.api import List

# Local imports
from example_task import ExampleTask


logger = logging.getLogger(__name__)


class ExamplePlugin(Plugin):

    #### 'IPlugin' interface ##############################################

    # The plugin's unique identifier.
    id = 'example.plugins.ipython_kernel'

    # The plugin's name (suitable for displaying to the user).
    name = 'IPython Kernel Example Plugin'

    #### Contributions to extension points made by this plugin ############

    kernel_namespace = List(contributes_to='ipython_plugin.namespace')

    def _kernel_namespace_default(self):
        namespace = [('app', self.application)]
        return namespace

    tasks = List(contributes_to='envisage.ui.tasks.tasks')

    def _tasks_default(self):
        print('Default tasks')
        return [
            TaskFactory(
                id='example_task',
                name='Example task',
                factory=ExampleTask
            )
        ]


class ExampleApplication(TasksApplication):

    #### 'IApplication' interface #########################################

    # The application's globally unique identifier.
    id = 'example.ipython_kernel'

    # The application's user-visible name.
    name = 'Example app'

    always_use_default_layout = True

    #### 'TasksApplication' interface #####################################

    # The default application-level layout for the application.
    default_layout = [
        TaskWindowLayout('example_task', size=(800, 600))
    ]

    def run(self):
        """ Run the application.

        Returns
        -------
        bool
            Whether the application started successfully (i.e., without a
            veto).
        """
        # Make sure the GUI has been created (so that, if required, the splash
        # screen is shown).
        gui = self.gui

        started = self.start()
        if started:
            app = get_app_qt4([''])

            # Create windows from the default or saved application layout.
            self._create_windows()

            kernel = self.get_service(IPYTHON_KERNEL_PROTOCOL)
            kernel.init_ipkernel('qt4')

            app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
                        app, QtCore.SLOT("quit()"))
            app.aboutToQuit.connect(kernel.cleanup_consoles)

            gui.set_trait_later(self, 'application_initialized', self)
            kernel.ipkernel.start()

        return started

    def _application_initialized_fired(self):
        logger.info('APPLICATION INITIALIZED')

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    app = ExampleApplication(
        plugins=[
            CorePlugin(), ExamplePlugin(), IPythonKernelPlugin(),
            IPythonKernelUIPlugin(), TasksPlugin(),
        ]
    )
    app.run()
