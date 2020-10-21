# Enthought library imports.
from traits.api import Enum, Str

# Local imports.
from attractors.model.i_model_2d import IModel2d


class IPlottable2d(IModel2d):

    plot_type = Enum("line", "scatter")

    x_label = Str
    y_label = Str
