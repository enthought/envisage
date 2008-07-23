""" A test class used in the service registry tests! """


# Enthought library imports.
from enthought.traits.api import HasTraits, implements

# Local imports.
from i_foo import IFoo


class Foo(HasTraits):
    implements(IFoo)


#### EOF ######################################################################
