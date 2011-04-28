# Enthought library imports.
from traits.api import Array, Interface, Unicode


class IModel2d(Interface):

    # The user-visible name of the model.
    name = Unicode

    x_data = Array
    y_data = Array
