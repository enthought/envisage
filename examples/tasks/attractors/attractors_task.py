# Enthought library imports.
from enthought.pyface.tasks.api import Task
from enthought.traits.api import List

# Local imports.
from plot_2d_pane import Plot2DPane


class AttractorsTask(Task):
    """ A task for viewing and tweaking attractors.
    """

    #### 'Task' interface #####################################################

    id = 'example.attractors_task'
    name = 'Attractors'

    #### 'AttractorsTask' interface ###########################################

    # The list of available attractor models.
    attractors = List

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def create_center_pane(self):
        return Plot2DPane(model=self.attractors[0])

    def create_dock_panes(self):
        return []

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _attractors_default(self):
        from model.lorenz import Lorenz
        return [ Lorenz() ]
