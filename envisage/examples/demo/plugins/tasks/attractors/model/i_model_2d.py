# Enthought library imports.
from traits.api import Array, Interface, Str


class IModel2d(Interface):

    # The user-visible name of the model.
    name = Str

    x_data = Array
    y_data = Array
