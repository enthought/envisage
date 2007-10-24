""" Tests for extension points. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint
from enthought.envisage.api import ExtensionRegistry
from enthought.traits.api import HasTraits, Int, List, TraitError


class ExtensionPointTestCase(unittest.TestCase):
    """ Tests for extension  points. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.registry = Application(extension_registry=ExtensionRegistry())
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################
        
    def test_untyped_extension_point(self):
        """ untyped extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', [42, 'a string', True])

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.assertEqual(3, len(f.x))
        self.assertEqual([42, 'a string', True],  f.x)

        g = Foo()
        self.assertEqual(3, len(g.x))
        self.assertEqual([42, 'a string', True],  g.x)
        
        return

    def test_typed_extension_point(self):
        """ typed extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', [42, 43, 44])

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.assertEqual(3, len(f.x))
        self.assertEqual([42, 43, 44], f.x)

        g = Foo()
        self.assertEqual(3, len(g.x))
        self.assertEqual([42, 43, 44], g.x)

        return

    def test_invalid_extension_point(self):
        """ invalid extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', 'xxx')

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure we get a trait error because the type of the extension
        # doesn't match that of the extension point.
        f = Foo()
        self.failUnlessRaises(TraitError, getattr, f, 'x')
        
        return

    def test_extension_point_with_no_id(self):
        """ extension point with no Id """

        registry = self.registry

        def factory():
            class Foo(HasTraits):
                x = ExtensionPoint(List(Int))
            
        self.failUnlessRaises(ValueError, factory)
            
        return

    def test_set_untyped_extension_point(self):
        """ set untyped extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(id='my.ep')

        # Make sure that when we set the trait the extension registry gets
        # updated.
        f = Foo()
        f.x = [42]
        
        self.assertEqual([42], registry.get_extensions('my.ep'))
        
        return

    def test_set_typed_extension_point(self):
        """ set typed extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that when we set the trait the extension registry gets
        # updated.
        f = Foo()
        f.x = [42]
        
        self.assertEqual([42], registry.get_extensions('my.ep'))
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=''):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc) 


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
