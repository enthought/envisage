# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""

This module offers mixin classes for testing implementations of
``IExtensionRegistry``.

All mixin classes should be complementary.
"""

import contextlib

# Enthought library imports.
from envisage.api import ExtensionPoint
from envisage.api import UnknownExtensionPoint
from traits.api import List


class ExtensionRegistryTestMixin:
    """ Base set of tests for testing generic functionality on
    ``IExtensionRegistry`` without depending on
    ``IExtensionRegistry.set_extensions`` (for historical reasons).

    Test cases inheriting from this mixin should define a setUp method that
    defines self.registry as an instance that implements IExtensionRegistry.
    """

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
        registry.add_extension_point(self.create_extension_point("my.ep"))

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
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # Make sure we can get it.
        extension_point = registry.get_extension_point("my.ep")
        self.assertNotEqual(None, extension_point)
        self.assertEqual("my.ep", extension_point.id)

    def test_get_extension_point_return_none_if_not_found(self):
        """ get extension point return None if id is not found. """
        self.assertIsNone(self.registry.get_extension_point("i.do.not.exist"))

    def test_get_extensions_mutation_no_effect_if_undefined(self):
        """ test one cannot mutate the registry by mutating the list if id
        is undefined.
        """
        # The extension point with id "my.ep" has not been defined
        extensions = self.registry.get_extensions("my.ep")

        # when
        extensions.append([[1, 2]])

        # then
        # the registry is not affected.
        self.assertEqual(self.registry.get_extensions("my.ep"), [])

    def test_remove_empty_extension_point(self):
        """ remove empty_extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # ...and remove it!
        registry.remove_extension_point("my.ep")

        # Make sure there are no extension points.
        extension_points = registry.get_extension_points()
        self.assertEqual(0, len(extension_points))

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

    def create_extension_point(self, id, trait_type=List, desc=""):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc)


class SettableExtensionRegistryTestMixin:
    """ Base set of tests for functionality of ``IExtensionRegistry``
    that depends on ``IExtensionRegistry.set_extensions``.

    Test cases inheriting from this mixin should define a setUp method that
    defines self.registry as an instance that implements IExtensionRegistry.
    """

    def test_remove_non_empty_extension_point(self):
        """ remove non-empty extension point """

        registry = self.registry

        # Add an extension point...
        registry.add_extension_point(ExtensionPoint(id="my.ep"))

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
        """ set extensions """

        registry = self.registry

        # Add an extension *point*.
        registry.add_extension_point(self.create_extension_point("my.ep"))

        # Set some extensions.
        registry.set_extensions("my.ep", [1, 2, 3])

        # Make sure we can get them.
        self.assertEqual([1, 2, 3], registry.get_extensions("my.ep"))

    def test_get_nonempty_extensions(self):
        """ test get nonempty extensions after setting it. """

        registry = self.registry
        registry.add_extension_point(ExtensionPoint(id="my.ep"))
        registry.set_extensions("my.ep", [[1, 2], [3, 4]])

        # when
        extensions = registry.get_extensions("my.ep")

        # then
        self.assertEqual(extensions, [[1, 2], [3, 4]])

    def test_get_extensions_mutation_no_effect_if_defined(self):
        """ test one cannot mutate the returned extensions to mutate the
        registry.
        """
        registry = self.registry
        registry.add_extension_point(ExtensionPoint(id="my.ep"))
        registry.set_extensions("my.ep", [[1, 2], [3, 4]])

        # when
        registry.get_extensions("my.ep").append([[5, 6]])

        # then
        # the registry is not affected.
        self.assertEqual(
            self.registry.get_extensions("my.ep"), [[1, 2], [3, 4]]
        )

    def test_mutate_original_extensions_mutate_registry(self):
        """ if the original extensions was mutated, the registry is mutated.
        """
        # This may be a bug? But it is certainly the current behavior of
        # ExtensionRegistry.
        registry = self.registry
        registry.add_extension_point(ExtensionPoint(id="my.ep"))
        extensions = [[1, 2], [3, 4]]
        registry.set_extensions("my.ep", extensions)

        # when
        extensions.append([5, 6])

        # then
        self.assertEqual(
            registry.get_extensions("my.ep"), [[1, 2], [3, 4], [5, 6]]
        )

    def test_set_extensions_with_unknown_extension_point_id(self):
        """ Test set_extensions raises UnknownExtensionPoint
        if the extension point has not been added in the first place.
        """
        registry = self.registry
        with self.assertRaises(UnknownExtensionPoint):
            registry.set_extensions("i.do.not.exist", [[1]])


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


class ListeningExtensionRegistryTestMixin:
    """ Base set of tests for listener functionality of ``IExtensionRegistry``.

    Test cases inheriting from this mixin should define a setUp method that
    defines self.registry as an instance that implements IExtensionRegistry.
    """

    def get_object_with_listener_method(self):
        """ Return an object with a method that can be used as an
        extension point listener along with the event list for inspection
        in tests.

        Returns
        -------
        object : ListensToExtensionPoint
        events : list
            List for collecting events.
            Each item should be an instance of ExtensionPointChangedEvent
            if the code being tested is correct.
        """
        events = []
        return ListensToExtensionPoint(events), events

    def get_nonmethod_listener(self):
        """ Return a callable that can be used as an extension point listener
        along with the event list for inspection in tests.

        Returns
        -------
        listener : callable(registry, event)
        events : list
            List for collecting events.
            Each item should be an instance of ExtensionPointChangedEvent
            if the code being tested is correct.
        """
        events = []
        return make_function_listener(events), events

    def test_add_nonmethod_listener(self):
        """ test adding extension point listener and its outcome."""
        listener, events = self.get_nonmethod_listener()

        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point_listener(listener, "my.ep")

        with self.assertAppendsTo(events):
            self.registry.set_extensions("my.ep", [[1, 2, 3]])

        # then
        actual_event, = events
        self.assertEqual(actual_event.extension_point_id, "my.ep")
        self.assertIsNone(actual_event.index)
        self.assertEqual(actual_event.added, [[1, 2, 3]])
        self.assertEqual(actual_event.removed, [])

    def test_nonmethod_listener_lifetime(self):
        listener, events = self.get_nonmethod_listener()
        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point_listener(listener, "my.ep")

        # The listener should not kept alive by the registry.
        del listener

        with self.assertDoesNotModify(events):
            self.registry.set_extensions("my.ep", [4, 5, 6, 7])

    def test_add_nonmethod_listener_non_matching_id(self):
        """ test when the extension id does not match, listener is not fired.
        """
        listener, events = self.get_nonmethod_listener()

        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point(ExtensionPoint(id="my.ep2"))
        self.registry.add_extension_point_listener(listener, "my.ep")

        # setting a different extension should not fire listener
        with self.assertDoesNotModify(events):
            self.registry.set_extensions("my.ep2", [[]])

    def test_add_method_listener(self):
        obj, events = self.get_object_with_listener_method()
        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point_listener(obj.listener, "my.ep")

        # At this point, the bound method 'obj.listener' no longer
        # exists; it's already been garbage collected. Nevertheless, the
        # listener should still fire.
        with self.assertAppendsTo(events):
            self.registry.set_extensions("my.ep", [1, 2, 3])

    def test_add_extension_point_listener_none(self):
        """ Listen to all extension points if extension_point_id is none """

        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point(ExtensionPoint(id="my.ep2"))

        listener, events = self.get_nonmethod_listener()
        self.registry.add_extension_point_listener(listener, None)

        with self.assertAppendsTo(events):
            self.registry.set_extensions("my.ep2", [[]])

        with self.assertAppendsTo(events):
            self.registry.set_extensions("my.ep", [[]])

    def test_remove_nonmethod_listener(self):
        listener, events = self.get_nonmethod_listener()

        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point_listener(listener, "my.ep")
        self.registry.remove_extension_point_listener(listener, "my.ep")

        with self.assertDoesNotModify(events):
            self.registry.set_extensions("my.ep", [[4, 5, 6, 7]])

    def test_remove_method_listener(self):
        obj, events = self.get_object_with_listener_method()
        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))

        # The two occurences of `obj.listener` below refer to different
        # objects. Nevertheless, they _compare_ equal, so the removal
        # should still be effective.
        self.registry.add_extension_point_listener(obj.listener, "my.ep")
        self.registry.remove_extension_point_listener(obj.listener, "my.ep")

        with self.assertDoesNotModify(events):
            self.registry.set_extensions("my.ep", [1, 2, 3])

    def test_method_listener_lifetime(self):
        obj, events = self.get_object_with_listener_method()
        self.registry.add_extension_point(ExtensionPoint(id="my.ep"))
        self.registry.add_extension_point_listener(obj.listener, "my.ep")

        # Removing the last reference to the object should deactivate
        # the listener.
        del obj

        with self.assertDoesNotModify(events):
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
