""" Tests for the extension registry. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionsChangedEvent, ExtensionPoint
from enthought.envisage.api import ExtensionProvider, ExtensionRegistry
from enthought.traits.api import Event, Int, Interface, List    


class ExtensionRegistryTestCase(unittest.TestCase):
    """ Tests for the extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.extension_registry = ExtensionRegistry()

        # This allows the 'ExtensionPoint' trait type to be used as a more
        # convenient way to access an extension point.
        ExtensionPoint.extension_registry = self.extension_registry
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_providers(self):
        """ providers """

        registry = self.extension_registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.extension.point':
                    extensions = [42]

                else:
                    extensions = []

                return extensions

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.extension.point':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        # Now add the providers.
        registry.providers = [ProviderA(), ProviderB()]

        # Now we should get their extensions.
        extensions = registry.get_extensions('my.extension.point')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.extension.point', extension_points[0])

        return

    def test_extensions_changed(self):
        """ extensions changed """

        registry = self.extension_registry

        # A provider.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            x = List(Int)
            
            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.extension.point':
                    return self.x

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self.extensions_changed = ExtensionsChangedEvent(
                    extension_point = 'my.extension.point',
                    added           = event.added,
                    removed         = event.removed
                )

                return

        # Now add the provider.
        a = ProviderA(x=[42])
        registry.providers = [a]

        # Now we should get the extension.
        extensions = registry.get_extensions('my.extension.point')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Now set that trait that fires the event that lives in the house that
        # jack built ;^)
        a.x.append(43)
        
        # Now we should get the new extension.
        extensions = registry.get_extensions('my.extension.point')
        self.assertEqual(2, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)

        return
    
##     def test_empty_registry(self):
##         """ empty registry """

##         registry = self.extension_registry

##         # Make sure there are no extensions.
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(0, len(extensions))

##         # Make sure there are no extension points.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(0, len(extension_points))
        
##         return

##     def test_add_extension(self):
##         """ add extension """

##         registry = self.extension_registry

##         # Add an extension.
##         registry.add_extension('my.extension.point', 42)

##         # Make sure there's one and only one extension.
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(1, len(extensions))
##         self.assertEqual(42, extensions[0])

##         # Make sure there's one and only one extension point.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(1, len(extension_points))
##         self.assertEqual('my.extension.point', extension_points[0])

##         return

##     def test_add_extension_strict(self):
##         """ add extension strict """

##         registry = self.extension_registry

##         # Setting the registry 'strict' flag means that extension points must
##         # be explicitly added to the registry before being used.
##         registry.strict = True

##         # We shouldn't be able to add any extensions unless the extension
##         # point has been explicitly declared.
##         self.failUnlessRaises(
##             InvalidExtensionPoint,
##             registry.add_extension, 'my.extension.point', 42
##         )

##         # Add the extension point.
##         registry.add_extension_point('my.extension.point')

##         # Now we should be able to add the extension.
##         registry.add_extension('my.extension.point', 42)

##         # Make sure there's one and only one extension.
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(1, len(extensions))
##         self.assertEqual(42, extensions[0])

##         return

##     def test_add_extensions(self):
##         """ add extensions """

##         registry = self.extension_registry

##         # Add 2 extensions.
##         registry.add_extensions('my.extension.point', [42, 43])

##         # Make sure there's two and only two extensions!
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(2, len(extensions))
##         self.assert_(42 in extensions)
##         self.assert_(43 in extensions)

##         # Make sure there's one and only one extension point.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(1, len(extension_points))
##         self.assertEqual('my.extension.point', extension_points[0])

##         return
    
##     def test_add_extensions_strict(self):
##         """ add extensions strict """

##         registry = self.extension_registry

##         # Setting the registry 'strict' flag means that extension points must
##         # be explicitly added to the registry before being used.
##         registry.strict = True

##         # We shouldn't be able to add any extensions unless the extension
##         # point has been explicitly declared.
##         self.failUnlessRaises(
##             InvalidExtensionPoint,
##             registry.add_extensions, 'my.extension.point', [42, 43]
##         )

##         # Add the extension point.
##         registry.add_extension_point('my.extension.point')

##         # Now we should be able to add the extensions.
##         registry.add_extensions('my.extension.point', [42, 43])

##         # Make sure there's two and only two extensions!
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(2, len(extensions))
##         self.assert_(42 in extensions)
##         self.assert_(43 in extensions)

##         # Make sure there's one and only one extension point.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(1, len(extension_points))
##         self.assertEqual('my.extension.point', extension_points[0])

##         return

##     def test_add_extension_point(self):
##         """ add extension point """

##         registry = self.extension_registry

##         # Add an extension *point*.
##         registry.add_extension_point('my.extension.point')

##         # Make sure there's NO extensions.
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(0, len(extensions))

##         # Make sure there's one and only one extension point.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(1, len(extension_points))
##         self.assertEqual('my.extension.point', extension_points[0])

##         return
    
##     def test_remove_extension(self):
##         """ remove extension """

##         registry = self.extension_registry

##         # Add an extension...
##         registry.add_extension('my.extension.point', 42)

##         # ... and remove it!
##         registry.remove_extension('my.extension.point', 42)
        
##         # Make sure there are no extensions.
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(0, len(extensions))

##         # But the extension point still exists.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(1, len(extension_points))
##         self.assertEqual('my.extension.point', extension_points[0])

##         return

##     def test_remove_non_existent_extension(self):
##         """ remove non existent extension """

##         registry = self.extension_registry

##         self.failUnlessRaises(
##             ValueError,
##             registry.remove_extension, 'my.extension.point', 42
##         )

##         return

##     def test_remove_extensions(self):
##         """ remove extensions """

##         registry = self.extension_registry

##         # Add two extensions...
##         registry.add_extensions('my.extension.point', [42, 43])

##         # ... and remove them!
##         registry.remove_extensions('my.extension.point', [42, 43])

##         # Make sure there are no extensions.
##         extensions = registry.get_extensions('my.extension.point')
##         self.assertEqual(0, len(extensions))

##         # But the extension point still exists.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(1, len(extension_points))
##         self.assertEqual('my.extension.point', extension_points[0])

##         return

##     def test_remove_non_existent_extensions(self):
##         """ remove non existent extensions """

##         registry = self.extension_registry

##         self.failUnlessRaises(
##             ValueError,
##             registry.remove_extensions, 'my.extension.point', [42, 43]
##         )

##         return

##     def test_remove_extension_point(self):
##         """ remove extension point """

##         registry = self.extension_registry

##         # Add an extension *point*...
##         registry.add_extension_point('my.extension.point')

##         # ...and remove it!
##         registry.remove_extension_point('my.extension.point')
        
##         # Make sure there are no extension points.
##         extension_points = registry.get_extension_points()
##         self.assertEqual(0, len(extension_points))

##         return

##     def test_remove_non_existent_extension_point(self):
##         """ remove non existent extension point """

##         registry = self.extension_registry

##         self.failUnlessRaises(
##             KeyError,
##             registry.remove_extension_point, 'my.extension.point'
##         )

##         return

##     def test_specific_extension_listener(self):
##         """ specific extension listener. """

##         registry = self.extension_registry

##         def listener(registry, extension_point, added, removed):
##             """ Called when an extension point has changed. """

##             self.listener_called = (registry, extension_point, added, removed)

##             return
            
##         # Listen for extensions being added/removed to/from a specific
##         # extension point.
##         registry.add_extension_listener(listener, 'my.extension.point')

##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('my.extension.point', 42)

##         # Make sure the listener was called...
##         self.assertNotEqual(None, self.listener_called)

##         # ... with the rightr information!
##         registry, extension_point, added, removed = self.listener_called
        
##         self.assertEqual(registry, registry)
##         self.assertEqual('my.extension.point', extension_point)
##         self.assertEqual([42], added)
##         self.assertEqual([], removed)

##         # Remove an extension.
##         self.listener_called = None
##         registry.remove_extension('my.extension.point', 42)

##         # Make sure the listener was called...
##         self.assertNotEqual(None, self.listener_called)

##         # ... with the right information.
##         registry, extension_point, added, removed = self.listener_called
        
##         self.assertEqual(registry, registry)
##         self.assertEqual('my.extension.point', extension_point)
##         self.assertEqual([], added)
##         self.assertEqual([42], removed)

##         # Remove the listener.
##         registry.remove_extension_listener(listener, 'my.extension.point')

##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('my.extension.point', 42)

##         # Make sure the listener was NOT called.
##         self.assertEqual(None, self.listener_called)
        
##         return

##     def test_global_extension_listener(self):
##         """ global extension listener. """

##         registry = self.extension_registry

##         def listener(registry, extension_point, added, removed):
##             """ Called when an extension point has changed. """

##             self.listener_called = (registry, extension_point, added, removed)

##             return
            
##         # Listen for extensions being added/removed to/from any extension
##         # point.
##         registry.add_extension_listener(listener)

##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('my.extension.point', 42)

##         # Make sure the listener was called...
##         self.assertNotEqual(None, self.listener_called)

##         # ... with the right information.
##         registry, extension_point, added, removed = self.listener_called
        
##         self.assertEqual(registry, registry)
##         self.assertEqual('my.extension.point', extension_point)
##         self.assertEqual([42], added)
##         self.assertEqual([], removed)

##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('your.extension.point', 43)

##         # Make sure the listener was called...
##         self.assertNotEqual(None, self.listener_called)

##         # ... with the right information.
##         registry, extension_point, added, removed = self.listener_called
        
##         self.assertEqual(registry, registry)
##         self.assertEqual('your.extension.point', extension_point)
##         self.assertEqual([43], added)
##         self.assertEqual([], removed)

##         # Remove an extension.
##         self.listener_called = None
##         registry.remove_extension('my.extension.point', 42)

##         # Make sure the listener was called...
##         self.assertNotEqual(None, self.listener_called)

##         # ... with the right information.
##         registry, extension_point, added, removed = self.listener_called
        
##         self.assertEqual(registry, registry)
##         self.assertEqual('my.extension.point', extension_point)
##         self.assertEqual([], added)
##         self.assertEqual([42], removed)

##         # Remove the listener.
##         registry.remove_extension_listener(listener)

##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('my.extension.point', 42)

##         # Make sure the listener was NOT called.
##         self.assertEqual(None, self.listener_called)

##         return

##     def test_gced_specific_extension_listener(self):
##         """ gc'ed extension listener. """

##         registry = self.extension_registry

##         def listener(registry, extension_point, added, removed):
##             """ Called when an extension point has changed. """

##             self.listener_called = (registry, extension_point, added, removed)

##             return
            
##         # Listen for extensions being added/removed to/from a specific
##         # extension point.
##         registry.add_extension_listener(listener, 'my.extension.point')

##         # Delete the listener!
##         del listener
        
##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('my.extension.point', 42)

##         # Remove an extension.
##         registry.remove_extension('my.extension.point', 42)

##         # Make sure the listener was NOT called.
##         self.assertEqual(None, self.listener_called)

##         return

##     def test_gced_global_extension_listener(self):
##         """ gc'ed global extension listener. """

##         registry = self.extension_registry

##         def listener(registry, extension_point, added, removed):
##             """ Called when an extension point has changed. """

##             self.listener_called = (registry, extension_point, added, removed)

##             return
            
##         # Listen for extensions being added/removed to/from any extension
##         # point.
##         registry.add_extension_listener(listener)

##         # Delete the listener!
##         del listener

##         # Add an extension.
##         self.listener_called = None
##         registry.add_extension('my.extension.point', 42)

##         # Remove an extension.
##         registry.remove_extension('my.extension.point', 42)

##         # Make sure the listener was NOT called.
##         self.assertEqual(None, self.listener_called)

##         return

##     def test_remove_non_existent_listener(self):
##         """ remove non existent listener """

##         registry = self.extension_registry

##         def listener(registry, extension_point, added, removed):
##             """ Called when an extension point has changed. """

##             self.listener_called = (registry, extension_point, added, removed)

##             return

##         self.failUnlessRaises(
##             ValueError, registry.remove_extension_listener, listener
##         )

##         return

#### EOF ######################################################################
