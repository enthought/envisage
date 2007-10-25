""" A test class used in the service registry tests! """


# Enthought library imports.
from enthought.traits.api import HasTraits, Interface, implements


class IFoo(Interface):
    pass

class Foo(HasTraits):
    implements(IFoo)


#### EOF ######################################################################
