# Enthought library imports.
from enthought.traits.api import Enum, Unicode

# Local imports.
from i_model_2d import IModel2d


class IPlottable2d(IModel2d):

    plot_type = Enum('line', 'scatter')

    title = Unicode
    x_label = Unicode
    y_label = Unicode
