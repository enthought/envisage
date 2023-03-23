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

# Enthought library imports.
from chaco.api import ArrayPlotData, Plot
from enable.api import ComponentEditor

from pyface.tasks.api import TraitsTaskPane
from traits.api import (
    Dict,
    Instance,
    List,
    observe,
    on_trait_change,
    Property,
    Str,
)
from traitsui.api import EnumEditor, HGroup, Item, Label, UItem, View


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
            ("x", "y"),
            type=self.plot_type,
            name=self.title,
            marker="pixel",
            color="blue",
        )

        return plot

    @observe("x_data,y_data")
    def _update_plot_data(self, event):
        if event.name == "x_data":
            self.plot.data.set_data("x", event.new)
        else:
            self.plot.data.set_data("y", event.new)
        self.plot.invalidate_and_redraw()

    @observe("x_label,y_label")
    def _update_axis_label(self, event):
        if event.name == "x_label":
            self.plot.x_axis.title = event.new
        else:
            self.plot.y_axis.title = event.new
        self.plot.invalidate_and_redraw()

    @observe("active_model")
    def _update_plot_new_model(self, event):
        if event.old:
            self.plot.delplot(event.old.name)

        self.plot.data.set_data("x", event.new.x_data)
        self.plot.data.set_data("y", event.new.y_data)
        self.plot.plot(
            ("x", "y"),
            type=self.plot_type,
            name=self.title,
            marker="pixel",
            color="blue",
        )
        self.plot.invalidate_and_redraw()

    view = View(
        HGroup(
            Label("Model: "),
            Item("active_model", editor=EnumEditor(name="_enum_map")),
            show_labels=False,
        ),
        UItem("plot", editor=ComponentEditor()),
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
