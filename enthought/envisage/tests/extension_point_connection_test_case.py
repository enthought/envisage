""" Tests for extension point connections. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, ExtensionPointConnection
from enthought.envisage.api import MutableExtensionRegistry
from enthought.envisage.api import connect_extension_point
from enthought.traits.api import Bool, HasTraits, Int, List, Float, Str


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """
    
    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


class ExtensionPointConnectionTestCase(unittest.TestCase):
    """ Tests for extension point connections. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.extension_registry = MutableExtensionRegistry()
        ExtensionPointConnection.extension_registry = self.extension_registry
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_untyped_extension_point(self):
        """ untyped extension point """

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        f = Foo()
        f.on_trait_change(listener)

        # Make some connections.
        connect_extension_point(f, 'x', 'my.ep')
        
        # Make sure that the object was initialized properly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Add another extension.
        registry.add_extension('my.ep', 'a string')

        # Make sure that the object picked up the new extension...
        self.assertEqual(2, len(f.x))
        self.assert_(42 in f.x)
        self.assert_('a string' in f.x)

        # ... and that the correct trait change event was fired.
        self.assertEqual(f, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual(1, len(listener.new.added))
        self.assert_('a string' in listener.new.added)
        
        return

    def test_set_extensions_via_trait(self):
        """ set extensions via trait """

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        f = Foo()
        f.on_trait_change(listener)

        # Make some connections.
        connect_extension_point(f, 'x', 'my.ep')
        
        # Make sure that the object was initialized properly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Set the extensions.
        f.x = ['a string']

        # Make sure that the object picked up the new extension...
        self.assertEqual(1, len(f.x))
        self.assert_('a string' in f.x)

        self.assertEqual(1, len(registry.get_extensions('my.ep')))
        self.assert_('a string' in registry.get_extensions('my.ep'))

        # ... and that the correct trait change event was fired.
        self.assertEqual(f, listener.obj)
        self.assertEqual('x', listener.trait_name)
        self.assertEqual(1, len(listener.new))
        self.assert_('a string' in listener.new)
        
        return

    def test_set_extensions_via_registry(self):
        """ set extensions via registry """

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension.
        registry.add_extension('my.ep', 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        f = Foo()
        f.on_trait_change(listener)

        # Make some connections.
        connect_extension_point(f, 'x', 'my.ep')
        
        # Make sure that the object was initialized properly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Set the extensions.
        registry.set_extensions('my.ep', ['a string'])

        # Make sure that the object picked up the new extension...
        self.assertEqual(1, len(f.x))
        self.assert_('a string' in f.x)

        # ... and that the correct trait change event was fired.
        self.assertEqual(f, listener.obj)
        self.assertEqual('x', listener.trait_name)
        self.assertEqual(1, len(listener.new))
        self.assert_('a string' in listener.new)
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=''):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc) 

#### EOF ######################################################################
