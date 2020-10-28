# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the events fired when extension points are changed. """

# Standard library imports.
import unittest

# Local imports.
from envisage.api import ExtensionPointChangedEvent
from envisage.tests.test_application import (
    PluginA,
    PluginB,
    PluginC,
    TestApplication,
    listener,
)


class ExtensionPointChangedTestCase(unittest.TestCase):
    """ Tests for the events fired when extension points are changed. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # Make sure that the listener contents get cleand up before each test.
        listener.obj = None
        listener.trait_name = None
        listener.old = None
        listener.new = None

    def test_set_extension_point(self):
        """ set extension point """

        a = PluginA()

        application = TestApplication(plugins=[a])
        application.start()

        # Try to set the extension point.
        with self.assertRaises(SystemError):
            setattr(a, "x", [1, 2, 3])

    def test_mutate_extension_point_no_events(self):
        """ Mutation will not emit change event for name_items """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        a.on_trait_change(listener, "x_items")
        events = []
        a.observe(events.append, "x:items")

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # when
        with self.assertWarns(RuntimeWarning):
            a.x.append(42)

        # then
        self.assertIsNone(listener.obj)
        self.assertEqual(len(events), 0)

    def test_mutate_extension_point_then_modify_from_registry(self):
        """ Mutating the extension point does nothing and should not cause
        subsequent change event information to become inconsistent.
        """
        a = PluginA()
        b = PluginB()
        c = PluginC()

        a.on_trait_change(listener, "x_items")
        events = []
        a.observe(events.append, "x:items")

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # when
        with self.assertWarns(RuntimeWarning):
            a.x.clear()

        # then
        self.assertIsNone(listener.obj)
        self.assertEqual(len(events), 0)

        # when
        # Append a contribution.
        b.x.append(4)

        # then
        self.assertEqual(a.x, [1, 2, 3, 4, 98, 99, 100])
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 3)
        self.assertEqual(event.added, [4])
        self.assertEqual(event.removed, [])

    def test_append(self):
        """ append """

        a = PluginA()
        a.on_trait_change(listener, "x_items")
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Append a contribution.
        b.x.append(4)

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(7, len(extensions))
        self.assertEqual([1, 2, 3, 4, 98, 99, 100], extensions)

        # Make sure we pick up the new contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(7, len(extensions))
        self.assertEqual([1, 2, 3, 4, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual("x_items", listener.trait_name)
        self.assertEqual([4], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)

    def test_append_with_observe(self):
        """ append with observe """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        events = []
        a.observe(events.append, "x:items")

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Append a contribution.
        b.x.append(4)

        # then
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 3)
        self.assertEqual(event.added, [4])
        self.assertEqual(event.removed, [])

    def test_remove(self):
        """ remove """

        a = PluginA()
        a.on_trait_change(listener, "x_items")
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Remove a contribution.
        b.x.remove(3)

        # Make sure we pick up the correct contributions via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(5, len(extensions))
        self.assertEqual([1, 2, 98, 99, 100], extensions)

        # Make sure we pick up the correct contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(5, len(extensions))
        self.assertEqual([1, 2, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual("x_items", listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([3], listener.new.removed)
        self.assertEqual(2, listener.new.index)

    def test_remove_with_observe(self):
        """ remove with observing items change. """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        events = []
        a.observe(events.append, "x:items")

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Remove a contribution.
        b.x.remove(3)

        # then
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 2)
        self.assertEqual(event.added, [])
        self.assertEqual(event.removed, [3])

    def test_assign_empty_list(self):
        """ assign empty list """

        a = PluginA()
        a.on_trait_change(listener, "x_items")
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Assign an empty list to one of the plugin's contributions.
        b.x = []

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we pick up the correct contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual("x_items", listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index.start)
        self.assertEqual(3, listener.new.index.stop)

    def test_assign_empty_list_with_observe(self):
        """ assign an empty list to a plugin triggers a list change event."""

        a = PluginA()
        b = PluginB()
        c = PluginC()

        events = []
        a.observe(events.append, "x:items")

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Assign an empty list to one of the plugin's contributions.
        b.x = []

        # then
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.added, [])
        self.assertEqual(event.removed, [1, 2, 3])
        self.assertEqual(event.index, 0)

    def test_assign_non_empty_list(self):
        """ assign non-empty list """

        a = PluginA()
        a.on_trait_change(listener, "x_items")
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Assign a non-empty list to one of the plugin's contributions.
        b.x = [2, 4, 6, 8]

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(7, len(extensions))
        self.assertEqual([2, 4, 6, 8, 98, 99, 100], extensions)

        # Make sure we pick up the new contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(7, len(extensions))
        self.assertEqual([2, 4, 6, 8, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual("x_items", listener.trait_name)
        self.assertEqual([2, 4, 6, 8], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index.start)
        self.assertEqual(3, listener.new.index.stop)

    def test_assign_non_empty_list_with_observe(self):
        """ assign non-empty list """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        events = []
        a.observe(events.append, "x:items")

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Assign a non-empty list to one of the plugin's contributions.
        b.x = [2, 4, 6, 8]

        # then
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 0)
        self.assertEqual(event.added, [2, 4, 6, 8])
        self.assertEqual(event.removed, [1, 2, 3])

    def test_add_plugin(self):
        """ add plugin """

        a = PluginA()
        a.on_trait_change(listener, "x_items")
        b = PluginB()
        c = PluginC()

        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Now add the other plugin.
        application.add_plugin(c)

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual("x_items", listener.trait_name)
        self.assertEqual([98, 99, 100], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)

    def test_add_plugin_with_observe(self):
        """ add plugin with observe """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        events = []
        a.observe(events.append, "x:items")

        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b])
        application.start()

        # Now add the other plugin.
        application.add_plugin(c)

        # then
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 3)
        self.assertEqual(event.added, [98, 99, 100])
        self.assertEqual(event.removed, [])

    def test_remove_plugin(self):
        """ remove plugin """

        a = PluginA()
        a.on_trait_change(listener, "x_items")
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Now remove one plugin.
        application.remove_plugin(b)

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions("a.x")
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual("x_items", listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index)

    def test_remove_plugin_with_observe(self):
        """ remove plugin with observe """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        events = []
        a.observe(events.append, "x:items")

        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Now remove one plugin.
        application.remove_plugin(b)

        # then
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 0)
        self.assertEqual(event.added, [])
        self.assertEqual(event.removed, [1, 2, 3])

    def test_race_condition(self):
        """ Test the extension point being modified before the application
        starts, changes before starting the application are not notified.
        """
        a = PluginA()
        b = PluginB()
        c = PluginC()
        application = TestApplication(plugins=[a, b, c])

        events = []
        a.observe(events.append, "x:items")

        # This sets the cache.
        self.assertEqual(a.x, [1, 2, 3, 98, 99, 100])

        # Now we mutate the registry, but the application has not started.
        b.x = [4, 5, 6]

        # then
        self.assertEqual(a.x, [4, 5, 6, 98, 99, 100])
        # application has not started, no events.
        self.assertEqual(len(events), 0)

        # Now we start the application, which connects the listener.
        application.start()

        # Change the value again.
        b.x = [1, 2]

        # then
        self.assertEqual(a.x, [1, 2, 98, 99, 100])

        # The mutation occurred before application starting is not reported.
        self.assertEqual(len(events), 1)
        event, = events
        self.assertEqual(event.object, a.x)
        self.assertEqual(event.index, 0)
        self.assertEqual(event.added, [1, 2])
        self.assertEqual(event.removed, [4, 5, 6])


class TestExtensionPointChangedEvent(unittest.TestCase):
    """ Test ExtensionPointChangedEvent object."""

    def test_extension_point_change_event_str_representation(self):
        """ test string representation of the ExtensionPointChangedEvent class
        """
        desired_repr = ("ExtensionPointChangedEvent(extension_point_id={}, "
                        "index=0, removed=[], added=[])")
        ext_pt_changed_evt = ExtensionPointChangedEvent(extension_point_id=1)
        self.assertEqual(desired_repr.format(1), str(ext_pt_changed_evt))
        self.assertEqual(desired_repr.format(1), repr(ext_pt_changed_evt))
