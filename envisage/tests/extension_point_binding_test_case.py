""" Tests for extension point bindings. """


# Enthought library imports.
from envisage.api import ExtensionPoint
from envisage.api import bind_extension_point
from traits.api import HasTraits, List
from traits.testing.unittest_tools import unittest

# Local imports.
#
# We do these as absolute imports to allow nose to run from a different
# working directory.
from envisage.tests.mutable_extension_registry import (
    MutableExtensionRegistry
)


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


class ExtensionPointBindingTestCase(unittest.TestCase):
    """ Tests for extension point binding. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.extension_registry = MutableExtensionRegistry()

        # Use the extension registry for all extension points and bindings.
        ExtensionPoint.extension_registry = self.extension_registry

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

        # Make some bindings.
        bind_extension_point(f, 'x', 'my.ep')

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

        # Make some bindings.
        bind_extension_point(f, 'x', 'my.ep')

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

        # Make some bindings.
        bind_extension_point(f, 'x', 'my.ep')

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

    def test_explicit_extension_registry(self):
        """ explicit extension registry """

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

        # Create an empty extension registry use that in the binding.
        extension_registry = MutableExtensionRegistry()

        # Make some bindings.
        bind_extension_point(f, 'x', 'my.ep', extension_registry)

        # Make sure that we pick up the empty extension registry and not the
        # default one.
        self.assertEqual(0, len(f.x))

        return

    def test_should_be_able_to_bind_multiple_traits_on_a_single_object(self):

        registry = self.extension_registry

        # Add 2 extension points.
        registry.add_extension_point(self._create_extension_point('my.ep'))
        registry.add_extension_point(self._create_extension_point('another.ep'))

        # Declare a class that consumes both of the extension points.
        class Foo(HasTraits):
            x = List
            y = List

        f = Foo()

        # Bind two different traits on the object to the extension points.
        bind_extension_point(f, 'x', 'my.ep', registry)
        bind_extension_point(f, 'y', 'another.ep', registry)
        self.assertEqual(0, len(f.x))
        self.assertEqual(0, len(f.y))

        # Add some contributions to the extension points.
        registry.add_extension('my.ep', 42)
        registry.add_extensions('another.ep', [98, 99, 100])

        # Make sure both traits were bound correctly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(3, len(f.y))

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
