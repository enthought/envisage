""" A definition of a category to be added to a class. """


# Enthought library imports.
from traits.api import HasTraits, Str


class Category(HasTraits):
    """ A definition of a category to be added to a class. """

    #### 'Category' interface #################################################

    # The name of the category class (the class that you want to add).
    class_name = Str

    # The name of the class that you want to add the category to.
    target_class_name = Str

#### EOF ######################################################################
