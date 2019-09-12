""" Tests for the base extension registry. """


# Enthought library imports.
from envisage.api import Application, ExtensionPoint
from envisage.api import ExtensionRegistry, UnknownExtensionPoint
from traits.api import List
from traits.testing.unittest_tools import unittest


class ExtensionRegistryTestCase(unittest.TestCase):
    """ Tests for the base extension registry. """

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

    def test_empty_registry(self):
        """ empty registry """

        registry = self.registry

        # Make sure there are no extensions.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(0, len(extensions))

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        return

    def test_add_extension_point(self):
        """ add extension point """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Make sure there's NO extensions.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(0, len(extensions))

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('my.ep', extension_points[0].id)

        return

    def test_get_extension_point(self):
        """ get extension point """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Make sure we can get it.
        extension_point = registry.get_extension_point('my.ep')
        self.assertNotEqual(None, extension_point)
        self.assertEqual('my.ep', extension_point.id)

        return

    def test_remove_empty_extension_point(self):
        """ remove empty_extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # ...and remove it!
        registry.remove_extension_point('my.ep')

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        return

    def test_remove_non_empty_extension_point(self):
        """ remove non-empty extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # ... with some extensions...
        registry.set_extensions('my.ep', [42])

        # ...and remove it!
        registry.remove_extension_point('my.ep')

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # And that the extensions are gone too.
        self.assertEqual([], registry.get_extensions('my.ep'))

        return

    def test_remove_non_existent_extension_point(self):
        """ remove non existent extension point """

        registry = self.registry

        self.failUnlessRaises(
            UnknownExtensionPoint, registry.remove_extension_point, 'my.ep'
        )

        return

    def test_remove_non_existent_listener(self):
        """ remove non existent listener """

        registry = self.registry

        def listener(registry, extension_point, added, removed, index):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

            return

        self.failUnlessRaises(
            ValueError, registry.remove_extension_point_listener, listener
        )

        return

    def test_set_extensions(self):
        """ set extensions """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set some extensions.
        registry.set_extensions('my.ep', [1, 2, 3])

        # Make sure we can get them.
        self.assertEqual([1, 2, 3], registry.get_extensions('my.ep'))

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
