# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the events fired when extension points are changed. """


# Enthought library imports.
from traits.testing.unittest_tools import unittest

# Local imports.
from envisage.tests.test_application import (
    PluginA, PluginB, PluginC, TestApplication, listener
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

    def test_append(self):
        """ append """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Append a contribution.
        b.x.append(4)

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions('a.x')
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
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([4], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)

    def test_remove(self):
        """ remove """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Remove a contribution.
        b.x.remove(3)

        # Make sure we pick up the correct contributions via the application.
        extensions = application.get_extensions('a.x')
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
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([3], listener.new.removed)
        self.assertEqual(2, listener.new.index)

    def test_assign_empty_list(self):
        """ assign empty list """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Assign an empty list to one of the plugin's contributions.
        b.x = []

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
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
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index.start)
        self.assertEqual(3, listener.new.index.stop)

    def test_assign_empty_list_no_event(self):
        """ assign empty list no event """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Assign an empty list to one of the plugin's contributions.
        b.x = []

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
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
        self.assertEqual(None, listener.obj)

    def test_assign_non_empty_list(self):
        """ assign non-empty list """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: If the extension point has not been accessed then the
        # provider extension registry can't work out what has changed, so it
        # won't fire a changed event.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Assign a non-empty list to one of the plugin's contributions.
        b.x = [2, 4, 6, 8]

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions('a.x')
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
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([2, 4, 6, 8], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index.start)
        self.assertEqual(4, listener.new.index.stop)

    def test_add_plugin(self):
        """ add plugin """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
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
        extensions = application.get_extensions('a.x')
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
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([98, 99, 100], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)

    def test_remove_plugin(self):
        """ remove plugin """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
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
        extensions = application.get_extensions('a.x')
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
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index)
