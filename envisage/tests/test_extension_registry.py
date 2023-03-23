# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the base extension registry. """

# Standard library imports.
import contextlib
import unittest

from traits.api import List

# Enthought library imports.
from envisage.api import Application, ExtensionPoint, ExtensionRegistry
from envisage.tests.test_extension_registry_mixin import (
    ExtensionRegistryTestMixin,
)


class ExtensionRegistryTestCase(ExtensionRegistryTestMixin, unittest.TestCase):
    """Tests for the base extension registry."""

    def setUp(self):
        """Prepares the test fixture before each test method is called."""

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.registry = Application(extension_registry=ExtensionRegistry())

    def test_remove_non_empty_extension_point(self):
        """remove non-empty extension point"""

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # ... with some extensions...
        registry.set_extensions("my.ep", [42])

        # ...and remove it!
        registry.remove_extension_point("my.ep")

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # And that the extensions are gone too.
        self.assertEqual([], registry.get_extensions("my.ep"))

    def test_set_extensions(self):
        """set extensions"""

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # Set some extensions.
        registry.set_extensions("my.ep", [1, 2, 3])

        # Make sure we can get them.
        self.assertEqual([1, 2, 3], registry.get_extensions("my.ep"))


def make_function_listener(events):
    """
    Return a simple non-method extension point listener.

    The listener appends events to the ``events`` list.
    """

    def listener(registry, event):
        events.append(event)

    return listener


class ListensToExtensionPoint:
    """
    Class with a method that can be used as an extension point listener.
    """

    def __init__(self, events):
        self.events = events

    def listener(self, registry, event):
        self.events.append(event)


class ExtensionPointListenerLifetimeTestCase(unittest.TestCase):
    def setUp(self):
        # We do all of the testing via the application to make sure it offers
        # the same interface!
        registry = Application(extension_registry=ExtensionRegistry())
        extension_point = ExtensionPoint(id="my.ep", trait_type=List())
        registry.add_extension_point(extension_point)
        self.registry = registry

        # A place to record events that listeners receive.
        self.events = []

    def test_add_nonmethod_listener(self):
        listener = make_function_listener(self.events)
        self.registry.add_extension_point_listener(listener, "my.ep")

        with self.assertAppendsTo(self.events):
            self.registry.set_extensions("my.ep", [1, 2, 3])

    def test_remove_nonmethod_listener(self):
        listener = make_function_listener(self.events)

        self.registry.add_extension_point_listener(listener, "my.ep")
        self.registry.remove_extension_point_listener(listener, "my.ep")

        with self.assertDoesNotModify(self.events):
            self.registry.set_extensions("my.ep", [4, 5, 6, 7])

    def test_nonmethod_listener_lifetime(self):
        listener = make_function_listener(self.events)
        self.registry.add_extension_point_listener(listener, "my.ep")

        # The listener should not kept alive by the registry.
        del listener

        with self.assertDoesNotModify(self.events):
            self.registry.set_extensions("my.ep", [4, 5, 6, 7])

    def test_add_method_listener(self):
        obj = ListensToExtensionPoint(self.events)
        self.registry.add_extension_point_listener(obj.listener, "my.ep")

        # At this point, the bound method 'obj.listener' no longer
        # exists; it's already been garbage collected. Nevertheless, the
        # listener should still fire.
        with self.assertAppendsTo(self.events):
            self.registry.set_extensions("my.ep", [1, 2, 3])

    def test_remove_method_listener(self):
        obj = ListensToExtensionPoint(self.events)
        # The two occurences of `obj.listener` below refer to different
        # objects. Nevertheless, they _compare_ equal, so the removal
        # should still be effective.
        self.registry.add_extension_point_listener(obj.listener, "my.ep")
        self.registry.remove_extension_point_listener(obj.listener, "my.ep")

        with self.assertDoesNotModify(self.events):
            self.registry.set_extensions("my.ep", [1, 2, 3])

    def test_method_listener_lifetime(self):
        obj = ListensToExtensionPoint(self.events)
        self.registry.add_extension_point_listener(obj.listener, "my.ep")

        # Removing the last reference to the object should deactivate
        # the listener.
        del obj

        with self.assertDoesNotModify(self.events):
            self.registry.set_extensions("my.ep", [1, 2, 3])

    # Helper assertions #######################################################

    @contextlib.contextmanager
    def assertAppendsTo(self, some_list):
        """
        Assert that exactly one element is appended to a list.

        Return a context manager that checks that the code in the corresponding
        with block appends exactly one element to the given list.
        """
        old_length = len(some_list)
        yield
        new_length = len(some_list)
        diff = new_length - old_length
        self.assertEqual(
            diff,
            1,
            msg="Expected exactly one new element; got {}".format(diff),
        )

    @contextlib.contextmanager
    def assertDoesNotModify(self, some_list):
        """
        Assert that a list is unchanged.

        Return a context manager that checks that the code in the corresponding
        with block does not modify the length of the given list.
        """
        old_length = len(some_list)
        yield
        new_length = len(some_list)
        diff = new_length - old_length
        self.assertEqual(
            diff,
            0,
            msg="Expected no new elements; got {}".format(diff),
        )
