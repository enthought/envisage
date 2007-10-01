""" Tests for the extension registry. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionProvider, ExtensionRegistry
from enthought.traits.api import Int, List    


class ExtensionProviderTestCase(unittest.TestCase):
    """ Tests for the extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.extension_registry = ExtensionRegistry()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_unsupported_methods(self):
        """ unsupported methods """

        r = self.extension_registry
        
        self.failUnlessRaises(NotImplementedError, r.add_extension, 'x', 42)
        self.failUnlessRaises(NotImplementedError, r.add_extensions, 'x', [42])
        self.failUnlessRaises(NotImplementedError, r.remove_extension, 'x', 42)
        self.failUnlessRaises(NotImplementedError, r.set_extensions, 'x', [42])

        return
    
    def test_providers(self):
        """ providers """

        extension_registry = self.extension_registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    extensions = [42]

                else:
                    extensions = []

                return extensions

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        # Add the providers to the registry.
        extension_registry.add_providers([ProviderA(), ProviderB()])

        # The provider's extensions should now be in the registry.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        # Make sure there's one and only one extension point.
        extension_points = extension_registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.point', extension_points[0])

        return

    def test_provider_extensions_changed(self):
        """ provider extensions changed """

        extension_registry = self.extension_registry

        # A provider.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            x = List(Int)
            
            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    return self.x

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extensions_changed(
                    'my.point', event.added, event.removed, event.index
                )
                
                return

        # Add the provider to the registry.
        a = ProviderA(x=[42])
        extension_registry.add_provider(a)

        # The provider's extensions should now be in the registry.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, extension_point, added, removed, index):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = extension_point
            listener.added = added
            listener.removed = removed
            listener.index = index

            return

        extension_registry.add_extension_listener(
            listener, 'my.point'
        )
        
        # Add a new extension via the provider.
        a.x.append(43)

        # Make sure the listener got called.
        self.assertEqual('my.point', listener.extension_point)
        self.assertEqual([43], listener.added)
        self.assertEqual([], listener.removed)
        
        # Now we should get the new extension.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(2, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)

        return

    def test_add_provider(self):
        """ add provider """

        extension_registry = self.extension_registry

        # A provider.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    return [42]

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extensions_changed(
                    'my.point', event.added, event.removed, event.index
                )
                
                return

        # Add the provider to the registry.
        extension_registry.add_provider(ProviderA())

        # The provider's extensions should now be in the registry.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, extension_point, added, removed, index):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = extension_point
            listener.added = added
            listener.removed = removed
            listener.index = index

            return

        extension_registry.add_extension_listener(
            listener, 'my.point'
        )

        # Add a new provider.
        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        extension_registry.add_provider(ProviderB())

        # Make sure the listener got called.
        self.assertEqual('my.point', listener.extension_point)
        self.assertEqual([43, 44], listener.added)
        self.assertEqual([], listener.removed)
        
        # Now we should get the new extensions.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        return

    def test_remove_provider(self):
        """ remove provider """

        extension_registry = self.extension_registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    return [42]

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extensions_changed(
                    'my.point', event.added, event.removed, event.index
                )
                
                return

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.point':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        # Add the providers to the registry.
        a = ProviderA()
        b = ProviderB()
        extension_registry.add_providers([a, b])

        # The provider's extensions should now be in the registry.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, extension_point, added, removed, index):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = extension_point
            listener.added = added
            listener.removed = removed

            return

        extension_registry.add_extension_listener(listener, 'my.point')

        # Remove one of the providers.
        extension_registry.remove_provider(b)

        # Make sure the listener got called.
        self.assertEqual('my.point', listener.extension_point)
        self.assertEqual([], listener.added)
        self.assertEqual([43, 44], listener.removed)
        
        # Make sure we don't get the removed extensions.
        extensions = extension_registry.get_extensions('my.point')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        return

#### EOF ######################################################################
