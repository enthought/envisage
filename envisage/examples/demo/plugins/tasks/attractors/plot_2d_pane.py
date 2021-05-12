# Enthought library imports.
from enable.api import ComponentEditor
from chaco.api import ArrayPlotData, Plot
from chaco.chaco_plot_editor import ChacoPlotItem
from pyface.tasks.api import TraitsTaskPane
from traits.api import (
    Dict,
    Enum,
    Instance,
    List,
    Property,
    Str,
    observe,
    on_trait_change,
)
from traitsui.api import EnumEditor, HGroup, Item, Label, UItem, View

# Local imports.
from attractors.model.i_plottable_2d import IPlottable2d


class Plot2dPane(TraitsTaskPane):

    #### 'ITaskPane' interface ################################################

    id = "example.attractors.plot_2d_pane"
    name = "Plot 2D Pane"

    #### 'Plot2dPane' interface ###############################################

    active_model = Instance(IPlottable2d)
    models = List(IPlottable2d)

    plot_type = Property(Str, observe="active_model.plot_type")
    title = Property(Str, observe="active_model.name")
    x_data = Property(observe="active_model.x_data")
    y_data = Property(observe="active_model.y_data")
    x_label = Property(Str, observe="active_model.x_label")
    y_label = Property(Str, observe="active_model.y_label")

    plot = Instance(Plot)

    def _plot_default(self):
        plot = Plot(ArrayPlotData(x=self.x_data, y=self.y_data))
        plot.x_axis.title = self.x_label
        plot.y_axis.title = self.y_label

        plot.plot(
            ("x", "y"), type=self.plot_type, name=self.title, marker='pixel', color="blue"
        )

        return plot

    @observe("x_data,y_data")
    def _update_plot_data(self, event):
        if event.name == "x_data":
            self.plot.data.set_data("x", self.x_data)
        else:
            self.plot.data.set_data("y", self.y_data)

    @observe("x_label,y_label")
    def _update_plot_data(self, event):
        if event.name == "x_label":
            self.plot.x_axis.title = event.new
        else:
            self.plot.y_axis.title = event.new

    @observe("active_model")
    def _update_plot_new_model(self, event):
        if event.old:
            self.plot.delplot(event.old.name)
        print(event.new.plot_type)
        self.plot.plot(
            ("x", "y"), type=event.new.plot_type, name=event.new.name, marker='pixel', color="blue"
        )
        print('heyyyy')
        self.plot.invalidate_and_redraw()
        print('yoooo')

    view = View(
        HGroup(
            Label("Model: "),
            Item("active_model", editor=EnumEditor(name="_enum_map")),
            show_labels=False,
        ),
        UItem(
            "plot", editor=ComponentEditor()
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
