# Enthought library imports.
from enthought.chaco.chaco_plot_editor import ChacoPlotItem
from enthought.pyface.tasks.api import TraitsTaskPane
from enthought.traits.api import Enum, DelegatesTo, Instance
from enthought.traits.ui.api import View

# Local imports.
from model.i_plottable_2d import IPlottable2D


class Plot2DPane(TraitsTaskPane):

    model = Instance(IPlottable2D, adapt='yes')
    
    plot_type = Enum('line', 'scatter')

    title = DelegatesTo('model')
    x_data = DelegatesTo('model')
    y_data = DelegatesTo('model')
    x_label = DelegatesTo('model')
    y_label = DelegatesTo('model')

    # FIXME: Replace with ComponentEditor for 'title' support.
    view = View(ChacoPlotItem('x_data', 'y_data',
                              show_label      = False,
                              resizable       = True,
                              orientation     = 'h',
                              type_trait      = 'plot_type',
                              title           = '',
                              x_label_trait   = 'x_label',
                              y_label_trait   = 'y_label',
                              color           = 'blue',
                              bgcolor         = 'white',
                              border_visible  = False ,
                              border_width    = 1),
                resizable = True)
