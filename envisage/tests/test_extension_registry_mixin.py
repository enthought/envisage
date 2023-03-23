# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Base set of tests for extension registry and its subclasses wrapped in a
mixin class.
"""

from traits.api import List

# Enthought library imports.
from envisage.api import ExtensionPoint, UnknownExtensionPoint


class ExtensionRegistryTestMixin:
    """Base set of tests for extension registry and its subclasses.

    Test cases inherriting from this mixin should define a setUp method that
    defines self.registry as an instance of ExtensionPointRegistry.
    """

    def test_empty_registry(self):
        """empty registry"""

        registry = self.registry

        # Make sure there are no extensions.
        extensions = registry.get_extensions("my.ep")
        self.assertEqual(0, len(extensions))

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

    def test_add_extension_point(self):
        """add extension point"""

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # Make sure there's NO extensions.
        extensions = registry.get_extensions("my.ep")
        self.assertEqual(0, len(extensions))

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual("my.ep", extension_points[0].id)

    def test_get_extension_point(self):
        """get extension point"""

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # Make sure we can get it.
        extension_point = registry.get_extension_point("my.ep")
        self.assertNotEqual(None, extension_point)
        self.assertEqual("my.ep", extension_point.id)

    def test_get_extension_point_return_none_if_not_found(self):
        """get extension point return None if id is not found."""
        self.assertIsNone(self.registry.get_extension_point("i.do.not.exist"))

    def test_get_extensions_mutation_no_effect_if_undefined(self):
        """test one cannot mutate the registry by mutating the list."""
        # The extension point with id "my.ep" has not been defined
        extensions = self.registry.get_extensions("my.ep")

        # when
        extensions.append([[1, 2]])

        # then
        # the registry is not affected.
        self.assertEqual(self.registry.get_extensions("my.ep"), [])

    def test_remove_empty_extension_point(self):
        """remove empty_extension point"""

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # ...and remove it!
        registry.remove_extension_point("my.ep")

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

    def test_remove_non_existent_extension_point(self):
        """remove non existent extension point"""

        registry = self.registry

        with self.assertRaises(UnknownExtensionPoint):
            registry.remove_extension_point("my.ep")

    def test_remove_non_existent_listener(self):
        """remove non existent listener"""

        registry = self.registry

        def listener(registry, extension_point, added, removed, index):
            """Called when an extension point has changed."""

            self.listener_called = (registry, extension_point, added, removed)

        with self.assertRaises(ValueError):
            registry.remove_extension_point_listener(listener)

    def create_extension_point(self, id, trait_type=List, desc=""):
        """Create an extension point."""

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc)
