#Enthought imports
from traits.api import HasTraits, Int, Str

class FactoryDefinition(HasTraits):
    """
    A project factory definition.

    An instance of the specified class is used to open and/or create new
    projects.

    The extension with the highest priority wins!  In the event of a tie,
    the first instance wins.

    """

    # The name of the class that implements the factory.
    class_name = Str

    # The priority of this factory
    priority = Int
