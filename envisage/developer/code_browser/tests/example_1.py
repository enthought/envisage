""" Example code used to test the code browser. """


# Enthought library imports.
from traits.api import HasTraits, Int



class Base(HasTraits):
    """ A class that inherits from 'Hastraits' directly. """

    # Some traits that explicitly specify a trait type.
    x = Int
    y = Int

    def foo(self):
        """ A method. """

    def bar(self):
        """ A method. """

#### EOF ######################################################################
