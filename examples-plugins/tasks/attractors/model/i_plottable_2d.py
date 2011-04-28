# Enthought library imports.
from traits.api import Enum, Unicode

# Local imports.
from i_model_2d import IModel2d


class IPlottable2d(IModel2d):

    plot_type = Enum('line', 'scatter')

    x_label = Unicode
    y_label = Unicode
