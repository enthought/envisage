""" Tests for extension points. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, ExtensionPointBinding
from enthought.envisage.api import MutableExtensionRegistry
from enthought.traits.api import HasTraits, Int, List, TraitError


class ExtensionPointTestCase(unittest.TestCase):
    """ Tests for extension  points. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.extension_registry = MutableExtensionRegistry()
        
        ExtensionPoint.extension_registry = self.extension_registry
        ExtensionPointBinding.extension_registry = self.extension_registry
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_extension_point_changed(self):
        """ extension point changed """

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(id='my.ep')

            def _x_changed(self, trait_name, old, new):
                """ Static trait change handler. """

                self.trait_name         = 'x'
                self.old                = old
                self.new                = new

                return

            def _x_items_changed(self, trait_name, old, new):
                """ Static trait change handler. """

                self.trait_name         = 'x_items'
                self.added              = new.added
                self.removed            = new.removed

                return
            
        # Make sure that instances of the class pick up the extensions.
        #
        # fixme: The bind call is a little weird - here. WHy wouldn't we just
        # use 'ExtensionPoint' trait types in plugins (where the wiring up can
        # be done in the base class), and then use 'ExtensionPointBinding's for
        # arbitrary classes.
        f = Foo(); f.trait('x').trait_type.bind(f, 'x')
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Add a new extension.
        registry.add_extension('my.ep', 43)

        # Make sure the correct trait change event was fired.
        self.assertEqual('x_items', f.trait_name)
        self.assertEqual([43], f.added)
        self.assertEqual([], f.removed)

        # Set the extension point.
        f.x = [99]

        # Make sure the correct trait change event was fired.
        self.assertEqual('x', f.trait_name)
        self.assertEqual([42, 43], f.old)
        self.assertEqual([99], f.new)
        
        return
        
    def test_untyped_extension_point(self):
        """ untyped extension point """

        registry = self.extension_registry

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

        registry = self.extension_registry

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

        registry = self.extension_registry

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

        registry = self.extension_registry

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

        registry = self.extension_registry

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

#### EOF ######################################################################
