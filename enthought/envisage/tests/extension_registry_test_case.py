""" Tests for the extension registry. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, ExtensionRegistry
    

class ExtensionRegistryTestCase(unittest.TestCase):
    """ Tests for the extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        ExtensionPoint.extension_registry = ExtensionRegistry()
        self.registry = ExtensionPoint.extension_registry

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################
        
    def test_empty_registry(self):
        """ empty registry """

        # Make sure there are no extensions.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(0, len(extensions))

        # fixme: Currently, just by getting the extensions we create an
        # extension point!!
##         # Make sure there are no extension points.
##         extension_points = self.registry.get_extension_points()
##         self.assertEqual(0, len(extension_points))
        
        return

    def test_add_extension(self):
        """ add extension """

        # Add an extension.
        self.registry.add_extension('my.extension.point', 42)

        # Make sure there's one and only one extension.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(1, len(extensions))
        self.assertEqual(42, extensions[0])

        # Make sure there's one and only one extension point.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    def test_add_extensions(self):
        """ add extensions """

        # Add two extensions.
        self.registry.add_extensions('my.extension.point', [42, 43])

        # Make sure there's two and only two extensions!
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(2, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)

        # Make sure there's one and only one extension point.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    # messin'...
    def test_add_extension_point(self):
        """ add extension point """

        # Add an extension *point*.
        self.registry.add_extension_point(
            'my.extension.point', type=List(Int), doc=""" Help """
        )

        # Make sure there's NO extensions.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(0, len(extensions))

        # Make sure there's one and only one extension point.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    def test_add_extension_point(self):
        """ add extension point """

        # Add an extension *point*.
        self.registry.add_extension_point('my.extension.point')

        # Make sure there's NO extensions.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(0, len(extensions))

        # Make sure there's one and only one extension point.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    def test_strict(self):
        """ strict """

        self.registry.strict = True

        # We shouldn't be able to add any extensions unless the extension
        # point has been explicitly declared.
        self.failUnlessRaises(
            ValueError, self.registry.add_extension, 'my.extension.point', 42
        )

        # Declare the extension point.
        self.registry.add_extension_point('my.extension.point')

        # Now we should be able to add the extension.
        self.registry.add_extension('my.extension.point', 42)

        # Make sure there's one and only one extension.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(1, len(extensions))
        self.assertEqual(42, extensions[0])

        return
    
    def test_remove_extension(self):
        """ remove extension """

        # Add an extension...
        self.registry.add_extension('my.extension.point', 42)

        # ... and remove it!
        self.registry.remove_extension('my.extension.point', 42)
        
        # Make sure there are no extensions.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(0, len(extensions))

        # But the extension point still exists.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    def test_remove_non_existent_extension(self):
        """ remove non existent extension """

        self.failUnlessRaises(
            ValueError,
            self.registry.remove_extension, 'my.extension.point', 42
        )

        return

    def test_remove_extensions(self):
        """ remove extensions """

        # Add two extensions...
        self.registry.add_extensions('my.extension.point', [42, 43])

        # ... and remove them!
        self.registry.remove_extensions('my.extension.point', [42, 43])

        # Make sure there are no extensions.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(0, len(extensions))

        # But the extension point still exists.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    def test_remove_non_existent_extensions(self):
        """ remove non existent extensions """

        self.failUnlessRaises(
            ValueError,
            self.registry.remove_extensions, 'my.extension.point', [42, 43]
        )

        return

    def test_remove_extension_point(self):
        """ remove extension point """

        # Add an extension *point*...
        self.registry.add_extension_point('my.extension.point')

        # ...and remove it!
        self.registry.remove_extension_point('my.extension.point')
        
        # Make sure there are no extension points.
        extension_points = self.registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # Add an extension *point* with some extensions...
        self.registry.add_extension_point('my.extension.point')
        self.registry.add_extension('my.extension.point', 42)
        
        # ...and remove it!
        self.registry.remove_extension_point('my.extension.point')
        
        # Make sure there are no extension points...
        extension_points = self.registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # ... and that the extensions got cleaned up too.
        extensions = self.registry.get_extensions('my.extension.point')
        self.assertEqual(0, len(extensions))
        
        return

    def test_remove_non_existent_extension_point(self):
        """ remove non existent extension point """

        self.failUnlessRaises(
            KeyError,
            self.registry.remove_extension_point, 'my.extension.point'
        )

        return

    def test_specific_extension_listener(self):
        """ specific extension listener. """

        def listener(registry, extension_point, added, removed):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

            return
            
        # Listen for extensions being added/removed to/from a specific
        # extension point.
        self.registry.add_extension_listener(listener, 'my.extension.point')

        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('my.extension.point', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the rightr information!
        registry, extension_point, added, removed = self.listener_called
        
        self.assertEqual(registry, self.registry)
        self.assertEqual('my.extension.point', extension_point)
        self.assertEqual([42], added)
        self.assertEqual([], removed)

        # Remove an extension.
        self.listener_called = None
        self.registry.remove_extension('my.extension.point', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point, added, removed = self.listener_called
        
        self.assertEqual(registry, self.registry)
        self.assertEqual('my.extension.point', extension_point)
        self.assertEqual([], added)
        self.assertEqual([42], removed)

        # Remove the listener.
        self.registry.remove_extension_listener(listener, 'my.extension.point')

        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('my.extension.point', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)
        
        return

    def test_global_extension_listener(self):
        """ global extension listener. """

        def listener(registry, extension_point, added, removed):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

            return
            
        # Listen for extensions being added/removed to/from any extension
        # point.
        self.registry.add_extension_listener(listener)

        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('my.extension.point', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point, added, removed = self.listener_called
        
        self.assertEqual(registry, self.registry)
        self.assertEqual('my.extension.point', extension_point)
        self.assertEqual([42], added)
        self.assertEqual([], removed)

        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('your.extension.point', 43)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point, added, removed = self.listener_called
        
        self.assertEqual(registry, self.registry)
        self.assertEqual('your.extension.point', extension_point)
        self.assertEqual([43], added)
        self.assertEqual([], removed)

        # Remove an extension.
        self.listener_called = None
        self.registry.remove_extension('my.extension.point', 42)

        # Make sure the listener was called...
        self.assertNotEqual(None, self.listener_called)

        # ... with the right information.
        registry, extension_point, added, removed = self.listener_called
        
        self.assertEqual(registry, self.registry)
        self.assertEqual('my.extension.point', extension_point)
        self.assertEqual([], added)
        self.assertEqual([42], removed)

        # Remove the listener.
        self.registry.remove_extension_listener(listener)

        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('my.extension.point', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)

        return

    def test_gced_specific_extension_listener(self):
        """ gc'ed extension listener. """

        def listener(registry, extension_point, added, removed):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

            return
            
        # Listen for extensions being added/removed to/from a specific
        # extension point.
        self.registry.add_extension_listener(listener, 'my.extension.point')

        # Delete the listener!
        del listener
        
        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('my.extension.point', 42)

        # Remove an extension.
        self.registry.remove_extension('my.extension.point', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)

        return

    def test_gced_global_extension_listener(self):
        """ gc'ed global extension listener. """

        def listener(registry, extension_point, added, removed):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

            return
            
        # Listen for extensions being added/removed to/from any extension
        # point.
        self.registry.add_extension_listener(listener)

        # Delete the listener!
        del listener

        # Add an extension.
        self.listener_called = None
        self.registry.add_extension('my.extension.point', 42)

        # Remove an extension.
        self.registry.remove_extension('my.extension.point', 42)

        # Make sure the listener was NOT called.
        self.assertEqual(None, self.listener_called)

        return

    def test_remove_non_existent_listener(self):
        """ remove non existent listener """

        def listener(registry, extension_point, added, removed):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

            return

        self.failUnlessRaises(
            ValueError,
            self.registry.remove_extension_listener, listener
        )

        return

#### EOF ######################################################################
