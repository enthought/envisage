""" Tests for the provider extension registry. """


# Standard imports
import unittest

# Enthought library imports.
from envisage.api import ExtensionPoint, ExtensionProvider
from envisage.api import ProviderExtensionRegistry
from traits.api import Int, List

# Local imports.
from .extension_registry_test_case import ExtensionRegistryTestCase


class ProviderExtensionRegistryTestCase(ExtensionRegistryTestCase):
    """ Tests for the provider extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.registry = ProviderExtensionRegistry()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_providers(self):
        """ providers """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """

                return [ExtensionPoint(List, 'x')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [42, 43]

                else:
                    extensions = []

                return extensions

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [44, 45, 46]

                else:
                    extensions = []

                return extensions

        class ProviderC(ExtensionProvider):
            """ An empty provider! """


        # Add the providers to the registry.
        registry.add_provider(ProviderA())
        registry.add_provider(ProviderB())
        registry.add_provider(ProviderC())

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(5, len(extensions))
        self.assertEqual(list(range(42, 47)), extensions)

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('x', extension_points[0].id)

        return

    def test_provider_extensions_changed(self):
        """ provider extensions changed """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            x = List(Int)

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """

                return [ExtensionPoint(List, 'my.ep')]

            def get_extensions(self, extension_point_id):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point_id == 'my.ep':
                    return self.x

                else:
                    extensions = []

                return extensions

            def _x_changed(self, old, new):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'my.ep', new, old, slice(0, len(old))
                )

                return

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'my.ep', event.added, event.removed, event.index
                )

                return


        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            x = List(Int)

            def get_extensions(self, extension_point_id):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point_id == 'my.ep':
                    return self.x

                else:
                    extensions = []

                return extensions

            def _x_changed(self, old, new):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'my.ep', new, old, slice(0, len(old))
                )

                return

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'my.ep', event.added, event.removed, event.index
                )

                return

        # Add the providers to the registry.
        a = ProviderA(x=[42])
        b = ProviderB(x=[99, 100])
        registry.add_provider(a)
        registry.add_provider(b)

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(3, len(extensions))
        self.assertEqual([42, 99, 100], extensions)

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed
            listener.index = event.index

            return

        registry.add_extension_point_listener(listener, 'my.ep')

        # Add a new extension via the provider.
        a.x.append(43)

        # Make sure the listener got called.
        self.assertEqual('my.ep', listener.extension_point)
        self.assertEqual([43], listener.added)
        self.assertEqual([], listener.removed)
        self.assertEqual(1, listener.index)

        # Now we should get the new extension.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(4, len(extensions))
        self.assertEqual([42, 43, 99, 100], extensions)

        # Insert a new extension via the other provider.
        b.x.insert(0, 98)

        # Make sure the listener got called.
        self.assertEqual('my.ep', listener.extension_point)
        self.assertEqual([98], listener.added)
        self.assertEqual([], listener.removed)
        self.assertEqual(2, listener.index)

        # Now we should get the new extension.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(5, len(extensions))
        self.assertEqual([42, 43, 98, 99, 100], extensions)

        # Completely change a provider's extensions.
        b.x = [1, 2]

        # Make sure the listener got called.
        self.assertEqual('my.ep', listener.extension_point)
        self.assertEqual([1, 2], listener.added)
        self.assertEqual([98, 99, 100], listener.removed)
        self.assertEqual(2, listener.index.start)
        self.assertEqual(5, listener.index.stop)

        # Now we should get the new extension.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(4, len(extensions))
        self.assertEqual([42, 43, 1, 2], extensions)

        return

    def test_add_provider(self):
        """ add provider """

        registry = self.registry

        # A provider.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """

                return [ExtensionPoint(List, 'x')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    return [42]

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'x', event.added, event.removed, event.index
                )

                return

        # Add the provider to the registry.
        registry.add_provider(ProviderA())

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed
            listener.index = event.index

            return

        registry.add_extension_point_listener(listener, 'x')

        # Add a new provider.
        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        registry.add_provider(ProviderB())

        # Make sure the listener got called.
        self.assertEqual('x', listener.extension_point)
        self.assertEqual([43, 44], listener.added)
        self.assertEqual([], listener.removed)

        # Now we should get the new extensions.
        extensions = registry.get_extensions('x')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        return

    def test_get_providers(self):
        """ get providers """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

        a = ProviderA()
        b = ProviderB()

        # Add the provider to the registry.
        registry.add_provider(a)
        registry.add_provider(b)

        # Make sure we can get them.
        self.assertEqual([a, b], registry.get_providers())

        return

    def test_remove_provider(self):
        """ remove provider """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """

                return [ExtensionPoint(List, 'x'), ExtensionPoint(List, 'y')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    return [42]

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'x', event.added, event.removed, event.index
                )

                return

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        # Add the providers to the registry.
        a = ProviderA()
        b = ProviderB()
        registry.add_provider(a)
        registry.add_provider(b)

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed

            return

        registry.add_extension_point_listener(listener, 'x')

        # Remove one of the providers.
        registry.remove_provider(b)

        # Make sure the listener got called.
        self.assertEqual('x', listener.extension_point)
        self.assertEqual([], listener.added)
        self.assertEqual([43, 44], listener.removed)

        # Make sure we don't get the removed extensions.
        extensions = registry.get_extensions('x')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Now remove the provider that declared the extension point.
        registry.remove_provider(a)

        # Make sure the extension point is gone.
        self.assertEqual(None, registry.get_extension_point('x'))

        # Make sure we don't get the removed extensions.
        extensions = registry.get_extensions('x')
        self.assertEqual(0, len(extensions))

        # Make sure the listener got called.
        self.assertEqual('x', listener.extension_point)
        self.assertEqual([], listener.added)
        self.assertEqual([42], listener.removed)

        return

    def test_remove_provider_with_no_contributions(self):
        """ remove provider with no contributions """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """

                return [ExtensionPoint(List, 'x'), ExtensionPoint(List, 'y')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                return []

        # Add the provider to the registry.
        a = ProviderA()
        registry.add_provider(a)

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(0, len(extensions))

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed

            return

        registry.add_extension_point_listener(listener, 'x')

        # Remove the provider that declared the extension point.
        registry.remove_provider(a)

        # Make sure the extension point is gone.
        self.assertEqual(None, registry.get_extension_point('x'))

        # Make sure we don't get the removed extensions.
        extensions = registry.get_extensions('x')
        self.assertEqual(0, len(extensions))

        # Make sure the listener did not get called  (since the provider did
        # not make any contributions anyway!).
        self.assertEqual(None, getattr(listener, 'registry', None))

        return

    def test_remove_non_existent_provider(self):
        """ remove provider """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            pass

        a = ProviderA()

        # Remove one of the providers.
        self.failUnlessRaises(ValueError, registry.remove_provider, a)

        return

    # Overriden to test differing behavior between the provider registry and
    # the base class.
    def test_set_extensions(self):
        """ set extensions """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set some extensions.
        self.failUnlessRaises(
            SystemError, registry.set_extensions, 'my.ep', [1, 2, 3]
        )

        return

    def test_remove_non_empty_extension_point(self):
        """ remove non-empty extension point """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """

                return [ExtensionPoint(List, 'x')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [42, 43]

                else:
                    extensions = []

                return extensions

        # Add the provider to the registry.
        registry.add_provider(ProviderA())

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(2, len(extensions))
        self.assertEqual(list(range(42, 44)), extensions)

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('x', extension_points[0].id)

        # Remove the extension point.
        registry.remove_extension_point('x')

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # And that the extensions are gone too.
        self.assertEqual([], registry.get_extensions('x'))

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
