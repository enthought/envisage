""" Tests for the extension registry. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, ExtensionProvider
from enthought.envisage.api import ExtensionRegistry
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

                self._fire_extensions_changed(
                    'my.extension.point', event.added, event.removed
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

#### EOF ######################################################################
