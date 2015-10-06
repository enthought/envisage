""" A test class used in the service registry tests! """


# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_foo import IFoo


@provides(IFoo)
class Foo(HasTraits):
    pass


#### EOF ######################################################################
