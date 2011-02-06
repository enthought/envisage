# Enthought library imports.
from enthought.pyface.tasks.action.api import SMenu, SMenuBar
from enthought.pyface.tasks.api import Task
from enthought.traits.api import Any, List

# Local imports.
from model.i_plottable_2d import IPlottable2D
from model_config_pane import ModelConfigPane
from plot_2d_pane import Plot2DPane


class AttractorsTask(Task):
    """ A task for viewing and tweaking attractors.
    """

    #### 'Task' interface #####################################################

    id = 'example.attractors.task'
    name = 'Attractors'

    menu_bar = SMenuBar(SMenu(id='View', name='View'))

    #### 'AttractorsTask' interface ###########################################

    # The attractor model that is currently active (visible in the center pane).
    active_model = Any

    # The list of available attractor models.
    models = List

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def create_central_pane(self):
        """ Create a plot pane with a list of models. Keep track of which model
            is active so that dock panes can introspect it.
        """
        pane = Plot2DPane(models=self.models)
        
        self.active_model = pane.active_model
        pane.on_trait_change(self._update_active_model, 'active_model')
        
        return pane

    def create_dock_panes(self):
        return [ ModelConfigPane(model=self.active_model) ]

    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _models_default(self):
        from model.lorenz import Lorenz
        from model.rossler import Rossler
        return [ Lorenz(), Rossler() ]

    #### Trait change handlers ################################################

    def _update_active_model(self):
        self.active_model = self.window.central_pane.active_model
        for dock_pane in self.window.dock_panes:
            dock_pane.model = self.active_model

