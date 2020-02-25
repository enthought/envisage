# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the base extension registry. """

import contextlib

# Enthought library imports.
from envisage.api import Application, ExtensionPoint
from envisage.api import ExtensionRegistry, UnknownExtensionPoint
from traits.api import List
from traits.testing.unittest_tools import unittest


class ExtensionRegistryTestCase(unittest.TestCase):
    """ Tests for the base extension registry. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.registry = Application(extension_registry=ExtensionRegistry())

    def test_empty_registry(self):
        """ empty registry """

        registry = self.registry

        # Make sure there are no extensions.
        extensions = registry.get_extensions("my.ep")
        self.assertEqual(0, len(extensions))

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

    def test_add_extension_point(self):
        """ add extension point """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Make sure there's NO extensions.
        extensions = registry.get_extensions("my.ep")
        self.assertEqual(0, len(extensions))

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual("my.ep", extension_points[0].id)

    def test_get_extension_point(self):
        """ get extension point """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Make sure we can get it.
        extension_point = registry.get_extension_point("my.ep")
        self.assertNotEqual(None, extension_point)
        self.assertEqual("my.ep", extension_point.id)

    def test_remove_empty_extension_point(self):
        """ remove empty_extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # ...and remove it!
        registry.remove_extension_point("my.ep")

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

    def test_remove_non_empty_extension_point(self):
        """ remove non-empty extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # ... with some extensions...
        registry.set_extensions("my.ep", [42])

        # ...and remove it!
        registry.remove_extension_point("my.ep")

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

        # And that the extensions are gone too.
        self.assertEqual([], registry.get_extensions("my.ep"))

    def test_remove_non_existent_extension_point(self):
        """ remove non existent extension point """

        registry = self.registry

        with self.assertRaises(UnknownExtensionPoint):
            registry.remove_extension_point("my.ep")

    def test_remove_non_existent_listener(self):
        """ remove non existent listener """

        registry = self.registry

        def listener(registry, extension_point, added, removed, index):
            """ Called when an extension point has changed. """

            self.listener_called = (registry, extension_point, added, removed)

        with self.assertRaises(ValueError):
            registry.remove_extension_point_listener(listener)

    def test_set_extensions(self):
        """ set extensions """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Set some extensions.
        registry.set_extensions("my.ep", [1, 2, 3])

        # Make sure we can get them.
        self.assertEqual([1, 2, 3], registry.get_extensions("my.ep"))

    def test_nonmethod_listener_lifetime(self):

        self.events = []

        def func_listener(registry, event):
            self.events.append(event)

        registry = self.registry
        registry.add_extension_point(self._create_extension_point("my.ep"))

        registry.add_extension_point_listener(func_listener, "my.ep")

        with self.assertAppendsTo(self.events):
            registry.set_extensions("my.ep", [1, 2, 3])

        # The listener should not kept alive by the registry.
        del func_listener

        with self.assertDoesNotModify(self.events):
            registry.set_extensions("my.ep", [4, 5, 6, 7])

    def test_nonmethod_listener_removal(self):
        self.events = []

        def func_listener(registry, event):
            self.events.append(event)

        registry = self.registry
        registry.add_extension_point(self._create_extension_point("my.ep"))
        registry.add_extension_point_listener(func_listener, "my.ep")

        with self.assertAppendsTo(self.events):
            registry.set_extensions("my.ep", [1, 2, 3])

        registry.remove_extension_point_listener(func_listener, "my.ep")

        with self.assertDoesNotModify(self.events):
            registry.set_extensions("my.ep", [4, 5, 6, 7])

    def test_method_listener_lifetime(self):
        self.events = []

        class ListensToExtensionPoint:
            def __init__(self, events):
                self.events = events

            def method_listener(self, registry, event):
                self.events.append(event)

        registry = self.registry
        registry.add_extension_point(self._create_extension_point("my.ep"))

        obj = ListensToExtensionPoint(self.events)
        registry.add_extension_point_listener(obj.method_listener, "my.ep")

        # At this point, the bound method 'obj.method_listener' no longer
        # exists; it's already been garbage collected. Nevertheless, the
        # listener should still fire.
        with self.assertAppendsTo(self.events):
            registry.set_extensions("my.ep", [1, 2, 3])

        # Removing the last reference to the object should deactivate
        # the listener.
        del obj

        with self.assertDoesNotModify(self.events):
            registry.set_extensions("my.ep", [1, 2, 3])

    def test_method_listener_removal(self):
        self.events = []

        class ListensToExtensionPoint:
            def __init__(self, events):
                self.events = events

            def method_listener(self, registry, event):
                self.events.append(event)

        registry = self.registry
        registry.add_extension_point(self._create_extension_point("my.ep"))

        obj = ListensToExtensionPoint(self.events)
        registry.add_extension_point_listener(obj.method_listener, "my.ep")

        with self.assertAppendsTo(self.events):
            registry.set_extensions("my.ep", [1, 2, 3])

        # Note that 'obj.method_listener' here is a different object from the
        # previous 'obj.method_listener'. But it compares equal to the
        # original, and that should be enough for removing the listener to
        # work.
        registry.remove_extension_point_listener(obj.method_listener, "my.ep")

        with self.assertDoesNotModify(self.events):
            registry.set_extensions("my.ep", [1, 2, 3])

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
            diff, 1,
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
            diff, 0,
            msg="Expected no new elements; got {}".format(diff),
        )

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=""):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc)
