""" Tests for the mutable extension registry. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, MutableExtensionRegistry
from enthought.envisage.api import UnknownExtensionPoint, UnknownExtension
from enthought.traits.api import List

# Local imports.
from extension_registry_test_case import ExtensionRegistryTestCase


class MutableExtensionRegistryTestCase(ExtensionRegistryTestCase):
    """ Tests for the mutable extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.registry = MutableExtensionRegistry()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_add_extension(self):
        """ add extension """

        registry = self.registry
        
        # We shouldn't be able to add an extension until the extension point
        # has been added.
        self.failUnlessRaises(
            UnknownExtensionPoint, registry.add_extension, 'my.ep', 42
        )

        # Add the extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Now we should be able to add an extension.
        registry.add_extension('my.ep', 42)

        # Make sure there's one and only one extension.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(1, len(extensions))
        self.assertEqual(42, extensions[0])

        return

    def test_add_extensions(self):
        """ add extensions """

        registry = self.registry
        
        # We shouldn't be able to add any extensions until the extension point
        # has been added.
        self.failUnlessRaises(
            UnknownExtensionPoint, registry.add_extensions, 'my.ep', [42, 43]
        )

        # Add the extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))
        
        # Now we should be able to add extensions.
        registry.add_extensions('my.ep', [42, 43])

        # Make sure there's two and only two extensions!
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(2, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)

        return
    
    def test_remove_extension(self):
        """ remove extension """

        registry = self.registry
        
        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add an extension...
        registry.add_extension('my.ep', 42)

        # ... and remove it!
        registry.remove_extension('my.ep', 42)
        
        # Make sure there are no extensions.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(0, len(extensions))

        # But the extension point still exists.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.ep', extension_points[0].id)

        return

    def test_remove_non_existent_extension(self):
        """ remove non existent extension """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        self.failUnlessRaises(
            UnknownExtension, registry.remove_extension, 'my.ep', 42
        )

        return

    def test_remove_extensions(self):
        """ remove extensions """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Add two extensions...
        registry.add_extensions('my.ep', [42, 43])

        # ... and remove them!
        registry.remove_extensions('my.ep', [42, 43])

        # Make sure there are no extensions...
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(0, len(extensions))

        # ... bu that the extension point still exists.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.ep', extension_points[0].id)

        return

    def test_remove_non_existent_extensions(self):
        """ remove non existent extensions """

        registry = self.registry
        
        # Add an extension point...
        registry.add_extension_point(self._create_extension_point('my.ep'))

        self.failUnlessRaises(
            UnknownExtension, registry.remove_extensions, 'my.ep', [42, 43]
        )

        return

    def test_remove_extension_point(self):
        """ remove extension point """

        registry = self.registry

        # Add an extension *point* with some extensions...
        registry.add_extension_point(self._create_extension_point('my.ep'))
        registry.add_extension('my.ep', 42)
        
        # ...and remove it!
        registry.remove_extension_point('my.ep')
        
        # Make sure there are no extension points...
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # ... and that the extensions got cleaned up too.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(0, len(extensions))
        
        return

    def test_specific_extension_point_listener(self):
        """ specific extension point listener. """

        registry = self.registry

        def listener(registry, event):
            """ Called when an extension point has changed. """

            self.listener_called = (
                registry, event.extension_point_id, event.added, event.removed
            )

            return

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))
            
        # Listen for extensions being added/removed to/from a specific
        # extension point.
        registry.add_extension_point_listener(listener, 'my.ep')

        # Add an extension.
        self.listener_called = None
        registry.add_extension('my.ep', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the rightr information!
        registry, extension_point_id, added, removed = self.listener_called
        
        self.assertEqual(registry, registry)
        self.assertEqual('my.ep', extension_point_id)
        self.assertEqual([42], added)
        self.assertEqual([], removed)

        # Remove an extension.
        self.listener_called = None
        registry.remove_extension('my.ep', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point_id, added, removed = self.listener_called
        
        self.assertEqual(registry, registry)
        self.assertEqual('my.ep', extension_point_id)
        self.assertEqual([], added)
        self.assertEqual([42], removed)

        # Remove the listener.
        registry.remove_extension_point_listener(listener, 'my.ep')

        # Add an extension.
        self.listener_called = None
        registry.add_extension('my.ep', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)
        
        return

    def test_global_extension_point_listener(self):
        """ global extension listener. """

        registry = self.registry

        def listener(registry, event):
            """ Called when an extension point has changed. """

            self.listener_called = (
                registry, event.extension_point_id, event.added, event.removed
            )

            return
            
        # Add some extension points.
        registry.add_extension_point(self._create_extension_point('my.ep'))
        registry.add_extension_point(self._create_extension_point('your.ep'))

        # Listen for extensions being added/removed to/from any extension
        # point.
        registry.add_extension_point_listener(listener)

        # Add an extension.
        self.listener_called = None
        registry.add_extension('my.ep', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point_id, added, removed = self.listener_called
        
        self.assertEqual(registry, registry)
        self.assertEqual('my.ep', extension_point_id)
        self.assertEqual([42], added)
        self.assertEqual([], removed)

        # Add an extension.
        self.listener_called = None
        registry.add_extension('your.ep', 43)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point_id, added, removed = self.listener_called
        
        self.assertEqual(registry, registry)
        self.assertEqual('your.ep', extension_point_id)
        self.assertEqual([43], added)
        self.assertEqual([], removed)

        # Remove an extension.
        self.listener_called = None
        registry.remove_extension('my.ep', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point_id, added, removed = self.listener_called
        
        self.assertEqual(registry, registry)
        self.assertEqual('my.ep', extension_point_id)
        self.assertEqual([], added)
        self.assertEqual([42], removed)

        # Remove the listener.
        registry.remove_extension_point_listener(listener)

        # Add an extension.
        self.listener_called = None
        registry.add_extension('my.ep', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)

        return

    def test_gced_specific_extension_point_listener(self):
        """ gc'ed extension point listener. """

        registry = self.registry

        def listener(registry, event):
            """ Called when an extension point has changed. """

            self.listener_called = (
                registry, event.extension_point, event.added, event.removed
            )

            return
            
        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Listen for extensions being added/removed to/from a specific
        # extension point.
        registry.add_extension_point_listener(listener, 'my.ep')

        # Delete the listener!
        del listener
        
        # Add an extension.
        self.listener_called = None
        registry.add_extension('my.ep', 42)

        # Remove an extension.
        registry.remove_extension('my.ep', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)

        return

    def test_gced_global_extension_point_listener(self):
        """ gc'ed global extension listener. """

        registry = self.registry

        def listener(registry, event):
            """ Called when an extension point has changed. """

            self.listener_called = (
                registry, event.extension_point, event.added, event.removed
            )

            return
            
        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Listen for extensions being added/removed to/from any extension
        # point.
        registry.add_extension_point_listener(listener)

        # Delete the listener!
        del listener

        # Add an extension.
        self.listener_called = None
        registry.add_extension('my.ep', 42)

        # Remove an extension.
        registry.remove_extension('my.ep', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)

        return

#### EOF ######################################################################
