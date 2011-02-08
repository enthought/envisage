# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.envisage.ui.tasks.api import TaskFactory
from enthought.traits.api import List

# Local imports.
from visualize_2d_task import Visualize2dTask


class AttractorsPlugin(Plugin):
    """ The chaotic attractors plugin.
    """

    # Extension point IDs.
    TASKS = 'enthought.envisage.ui.tasks.tasks'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'example.attractors'

    # The plugin's name (suitable for displaying to the user).
    name = 'Attractors'

    #### Contributions to extension points made by this plugin ################

    tasks = List(contributes_to=TASKS)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _tasks_default(self):
        return [ TaskFactory(id = 'example.attractors.task_2d',
                             name = '2D Visualization',
                             factory = Visualize2dTask) ]
