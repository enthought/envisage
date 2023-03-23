# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Local imports.
from attractors.model.i_plottable_2d import IPlottable2d
from attractors.model_config_pane import ModelConfigPane
from attractors.model_help_pane import ModelHelpPane
from attractors.plot_2d_pane import Plot2dPane

# Enthought library imports.
from pyface.tasks.action.api import SMenu, SMenuBar, TaskToggleGroup
from pyface.tasks.api import PaneItem, Tabbed, Task, TaskLayout
from traits.api import adapt, Any, Instance, List


class Visualize2dTask(Task):
    """A task for visualizing attractors in 2D."""

    #### 'Task' interface #####################################################

    id = "example.attractors.task_2d"
    name = "2D Visualization"

    menu_bar = SMenuBar(
        SMenu(id="File", name="&File"),
        SMenu(id="Edit", name="&Edit"),
        SMenu(TaskToggleGroup(), id="View", name="&View"),
    )

    #### 'Visualize2dTask' interface ##########################################

    # The attractor model that is currently active (visible in the center
    # pane).
    active_model = Any

    # The list of available attractor models.
    models = List(Instance(IPlottable2d))

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def create_central_pane(self):
        """Create a plot pane with a list of models. Keep track of which model
        is active so that dock panes can introspect it.
        """
        pane = Plot2dPane(models=self.models)

        self.active_model = pane.active_model
        pane.on_trait_change(self._update_active_model, "active_model")

        return pane

    def create_dock_panes(self):
        return [
            ModelConfigPane(model=self.active_model),
            ModelHelpPane(model=self.active_model),
        ]

    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _default_layout_default(self):
        return TaskLayout(
            left=Tabbed(
                PaneItem("example.attractors.model_config_pane"),
                PaneItem("example.attractors.model_help_pane"),
            )
        )

    def _models_default(self):
        from attractors.model.henon import Henon
        from attractors.model.lorenz import Lorenz
        from attractors.model.rossler import Rossler

        models = [Henon(), Lorenz(), Rossler()]

        return [adapt(model, IPlottable2d) for model in models]

    #### Trait change handlers ################################################

    def _update_active_model(self):
        self.active_model = self.window.central_pane.active_model
        for dock_pane in self.window.dock_panes:
            dock_pane.model = self.active_model
