# Enthought library imports.
from enthought.envisage.ui.tasks.api import TasksApplication
from enthought.pyface.tasks.api import TaskWindowLayout

# Plugin imports.
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.tasks.tasks_plugin import TasksPlugin
from attractors_plugin import AttractorsPlugin


class AttractorsApplication(TasksApplication):
    """ The chaotic attractors Tasks application.
    """

    #### 'IApplication' interface #############################################

    # The application's globally unique identifier.
    id = 'example.attractors'

    #### 'TasksApplication' interface #########################################

    # The default window-level layout for the application.
    default_layout = [ TaskWindowLayout(tasks=['example.attractors.task'],
                                        size=(800, 600)) ]


def main(argv):
    """ Run the application.
    """
    plugins = [ CorePlugin(), TasksPlugin(), AttractorsPlugin() ]
    app = AttractorsApplication(plugins=plugins)
    app.run()
    
    
if __name__ == '__main__':
    import sys
    main(sys.argv)
