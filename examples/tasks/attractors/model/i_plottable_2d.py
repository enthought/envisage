# Enthought library imports.
from enthought.traits.api import Array, Interface, Unicode


class IPlottable2D(Interface):

    x_data = Array
    y_data = Array

    title = Unicode
    x_label = Unicode
    y_label = Unicode
