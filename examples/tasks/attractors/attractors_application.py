# Enthought library imports.
from enthought.envisage.ui.tasks.api import TasksApplication
from enthought.pyface.tasks.api import TaskWindowLayout


class AttractorsApplication(TasksApplication):
    """ The chaotic attractors Tasks application.
    """

    #### 'IApplication' interface #############################################

    # The application's globally unique identifier.
    id = 'example.attractors'

    # The application's user-visible name.
    name = 'Attractors'

    #### 'TasksApplication' interface #########################################

    # The default window-level layout for the application.
    default_layout = [ TaskWindowLayout(tasks=['example.attractors.task_2d',
                                               'example.attractors.task_3d'],
                                        size=(800, 600)) ]
