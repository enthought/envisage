""" Tests for extension points. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, MutableExtensionRegistry
from enthought.traits.api import HasTraits, Int, List, TraitError


class ExtensionPointTestCase(unittest.TestCase):
    """ Tests for extension  points. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        ExtensionPoint.extension_registry = MutableExtensionRegistry()
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_untyped_extension_point(self):
        """ untyped extension point """

        registry = ExtensionPoint.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        g = Foo()
        self.assertEqual(1, len(g.x))
        self.assertEqual(42, g.x[0])

        # Add another extension.
        registry.add_extension('my.ep', 'a string')

        # Make sure that the existing instances of the class pick up the new
        # extension.
        self.assertEqual(2, len(f.x))
        self.assert_(42 in f.x)
        self.assert_('a string' in f.x)

        self.assertEqual(2, len(g.x))
        self.assert_(42 in g.x)
        self.assert_('a string' in g.x)
        
        return

    def test_typed_extension_point(self):
        """ typed extension point """

        registry = ExtensionPoint.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        g = Foo()
        self.assertEqual(1, len(g.x))
        self.assertEqual(42, g.x[0])

        # Add another extension.
        registry.add_extension('my.ep', 43)

        # Make sure that the existing instances of the class pick up the new
        # extension.
        self.assertEqual(2, len(f.x))
        self.assert_(42 in f.x)
        self.assert_(43 in f.x)

        self.assertEqual(2, len(g.x))
        self.assert_(42 in g.x)
        self.assert_(43 in g.x)
        
        return

    def test_invalid_extension_point(self):
        """ invalid extension point """

        registry = ExtensionPoint.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 'xxx')

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.failUnlessRaises(TraitError, getattr, f, 'x')
        
        return

    def test_set_untyped_extension_point(self):
        """ set untyped extension point """

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(id='my.ep')

        # Make sure that an exception gets raised when we try to access the
        # trait.
        f = Foo()
        self.failUnlessRaises(TraitError, setattr, f, 'x', [42])
        
        return

    def test_set_typed_extension_point(self):
        """ set typed extension point """

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that an exception gets raised when we try to access the
        # trait.
        f = Foo()
        self.failUnlessRaises(TraitError, setattr, f, 'x', [42])
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=''):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc) 

#### EOF ######################################################################
