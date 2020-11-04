# Enthought library imports.
from chaco.chaco_plot_editor import ChacoPlotItem
from pyface.tasks.api import TraitsTaskPane
from traits.api import (
    Dict,
    Enum,
    Instance,
    List,
    Property,
    Str,
    on_trait_change,
)
from traitsui.api import EnumEditor, HGroup, Item, Label, View

# Local imports.
from attractors.model.i_plottable_2d import IPlottable2d


class Plot2dPane(TraitsTaskPane):

    #### 'ITaskPane' interface ################################################

    id = "example.attractors.plot_2d_pane"
    name = "Plot 2D Pane"

    #### 'Plot2dPane' interface ###############################################

    active_model = Instance(IPlottable2d)
    models = List(IPlottable2d)

    plot_type = Property(Str, depends_on="active_model.plot_type")
    title = Property(Str, depends_on="active_model.name")
    x_data = Property(depends_on="active_model.x_data")
    y_data = Property(depends_on="active_model.y_data")
    x_label = Property(Str, depends_on="active_model.x_label")
    y_label = Property(Str, depends_on="active_model.y_label")

    view = View(
        HGroup(
            Label("Model: "),
            Item("active_model", editor=EnumEditor(name="_enum_map")),
            show_labels=False,
        ),
        ChacoPlotItem(
            "x_data",
            "y_data",
            show_label=False,
            resizable=True,
            orientation="h",
            marker="pixel",
            marker_size=1,
            type_trait="plot_type",
            title="",
            x_label_trait="x_label",
            y_label_trait="y_label",
            color="blue",
            bgcolor="white",
            border_visible=False,
            border_width=1,
        ),
        resizable=True,
    )

    #### Private traits #######################################################

    _enum_map = Dict(IPlottable2d, Str)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait property getters/setters #######################################

    def _get_plot_type(self):
        return self.active_model.plot_type if self.active_model else "line"

    def _get_title(self):
        return self.active_model.name if self.active_model else ""

    def _get_x_data(self):
        return self.active_model.x_data if self.active_model else []

    def _get_y_data(self):
        return self.active_model.y_data if self.active_model else []

    def _get_x_label(self):
        return self.active_model.x_label if self.active_model else ""

    def _get_y_label(self):
        return self.active_model.y_label if self.active_model else ""

    #### Trait change handlers ################################################

    @on_trait_change("models[]")
    def _update_models(self):
        # Make sure that the active model is valid with the new model list.
        if self.active_model not in self.models:
            self.active_model = self.models[0] if self.models else None

        # Refresh the EnumEditor map.
        self._enum_map = dict((model, model.name) for model in self.models)
