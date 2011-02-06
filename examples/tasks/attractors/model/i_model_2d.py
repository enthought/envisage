# Enthought library imports.
from enthought.traits.api import Array, Interface


class IModel2d(Interface):

    x_data = Array
    y_data = Array
