""" Tests to help find out if we can do type-safe casting. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.traits.api import HasTraits, Int, Interface, List, implements

# Local imports.
from cast import cast, ProtocolError


class ISuper(Interface):
    """ A base interface. """
    
    x = Int

class IFoo(ISuper):
    """ A derived interface. """
    
    y = Int
    
    def bar(self):
        """ A method! """


class Foo(HasTraits):
    """ A concrete implementation. """
    
    implements(IFoo)

    # 'ISuper' interface.
    x = Int(42)

    # 'IFoo' interface.
    y = Int(99)
    
    def bar(self):
        """ A method! """
        
        return 100

    
class CastTestCase(unittest.TestCase):
    """ Tests to help find out if we can do type-safe casting. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_attribute(self):
        """ attribute """

        f = cast(Foo(), IFoo)

        self.assertEqual(42, f.x)
        self.assertEqual(99, f.y)
        self.assertEqual(100, f.bar())

        return

    def test_protocol_error(self):
        """ protocol error """

        f = cast(Foo(), IFoo)

        self.failUnlessRaises(ProtocolError, getattr, f, 'bogus')

        return

#### EOF ######################################################################
