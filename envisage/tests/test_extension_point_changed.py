# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
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
from envisage.tests.support import PluginA, PluginB, PluginC, SimpleApplication


class ExtensionPointChangedTestCase(unittest.TestCase):
    """Tests for the events fired when extension points are changed."""

    def test_set_extension_point(self):
        """set extension point"""

        a = PluginA()

        application = SimpleApplication(plugins=[a])
        application.start()

        # Try to set the extension point.
        with self.assertRaises(TypeError):
            setattr(a, "x", [1, 2, 3])

    def test_mutate_extension_point_no_events(self):
        """Mutation will not emit change event for name_items"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
        application.start()

        # when
        a.x.append(42)

        # then
        self.assertEqual(events, [])

    def test_append(self):
        """append"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

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
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(a, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual([4], event.new.added)
        self.assertEqual([], event.new.removed)
        self.assertEqual(3, event.new.index)

    def test_remove(self):
        """remove"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

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
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(a, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual([], event.new.added)
        self.assertEqual([3], event.new.removed)
        self.assertEqual(2, event.new.index)

    def test_assign_empty_list(self):
        """assign empty list"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

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
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(a, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual([], event.new.added)
        self.assertEqual([1, 2, 3], event.new.removed)
        self.assertEqual(0, event.new.index.start)
        self.assertEqual(3, event.new.index.stop)

    def test_assign_empty_list_no_event(self):
        """assign empty list no event"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
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

        # We shouldn't get a trait event here because we haven't accessed the
        # extension point yet!
        self.assertEqual(events, [])

    def test_assign_non_empty_list(self):
        """assign non-empty list"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Keep the old values for later slicing check
        source_values = list(a.x)

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
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(a, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual([2, 4, 6, 8], event.new.added)
        self.assertEqual([1, 2, 3], event.new.removed)

        # The removed entry should match what the old values say
        self.assertEqual(event.new.removed, source_values[event.new.index])

        # If we use the index and apply the changes to the old list, we should
        # recover the new list
        source_values[event.new.index] = event.new.added
        self.assertEqual(source_values, application.get_extensions("a.x"))

        self.assertEqual(0, event.new.index.start)
        self.assertEqual(3, event.new.index.stop)

    def test_add_plugin(self):
        """add plugin"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        # Start off with just two of the plugins.
        application = SimpleApplication(plugins=[a, b])
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
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(a, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual([98, 99, 100], event.new.added)
        self.assertEqual([], event.new.removed)
        self.assertEqual(3, event.new.index)

    def test_remove_plugin(self):
        """remove plugin"""

        events = []

        a = PluginA()
        a.observe(events.append, "x_items")
        b = PluginB()
        c = PluginC()

        application = SimpleApplication(plugins=[a, b, c])
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
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(a, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual([], event.new.added)
        self.assertEqual([1, 2, 3], event.new.removed)
        self.assertEqual(0, event.new.index)

    def test_extension_point_change_event_str_representation(self):
        """
        test string representation of the ExtensionPointChangedEvent class
        """
        desired_repr = (
            "ExtensionPointChangedEvent(extension_point_id={}, "
            "index=0, removed=[], added=[])"
        )
        ext_pt_changed_evt = ExtensionPointChangedEvent(extension_point_id=1)
        self.assertEqual(desired_repr.format(1), str(ext_pt_changed_evt))
        self.assertEqual(desired_repr.format(1), repr(ext_pt_changed_evt))
