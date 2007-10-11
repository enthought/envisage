""" Tests for the base extension registry. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, ExtensionRegistry
from enthought.envisage.api import UnknownExtensionPoint, UnknownExtension
from enthought.traits.api import List


class ExtensionRegistryTestCase(unittest.TestCase):
    """ Tests for the base extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.registry = ExtensionRegistry()

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
    
    def test_remove_extension_point(self):
        """ remove extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # ...and remove it!
        registry.remove_extension_point('my.ep')
        
        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))
        
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

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=''):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc) 

#### EOF ######################################################################
