# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the plugin manager. """


# Standard library imports.
import unittest

from traits.api import Bool

# Enthought library imports.
from envisage.api import Plugin, PluginManager


class SimplePlugin(Plugin):
    """A simple plugin."""

    #### 'SimplePlugin' interface #############################################

    started = Bool(False)
    stopped = Bool(False)

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """Start the plugin."""

        self.started = True
        self.stopped = False

    def stop(self):
        """Stop the plugin."""

        self.started = False
        self.stopped = True


class BadPlugin(Plugin):
    """A plugin that just causes trouble ;^)."""

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """Start the plugin."""

        raise 1 / 0

    def stop(self):
        """Stop the plugin."""

        raise 1 / 0


class PluginManagerTestCase(unittest.TestCase):
    """Tests for the plugin manager."""

    def test_get_plugin(self):
        """get plugin"""

        simple_plugin = SimplePlugin()
        plugin_manager = PluginManager(plugins=[simple_plugin])

        # Get the plugin.
        plugin = plugin_manager.get_plugin(simple_plugin.id)
        self.assertEqual(plugin, simple_plugin)

        # Try to get a non-existent plugin.
        self.assertEqual(None, plugin_manager.get_plugin("bogus"))

    def test_iteration_over_plugins(self):
        """iteration over plugins"""

        simple_plugin = SimplePlugin()
        bad_plugin = BadPlugin()

        plugin_manager = PluginManager(plugins=[simple_plugin, bad_plugin])

        # Iterate over the plugin manager's plugins.
        plugins = []
        for plugin in plugin_manager:
            plugins.append(plugin)

        self.assertEqual([simple_plugin, bad_plugin], plugins)

    def test_start_and_stop(self):
        """start and stop"""

        simple_plugin = SimplePlugin()
        plugin_manager = PluginManager(plugins=[simple_plugin])

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        plugin_manager.start()

        # Make sure the plugin was started.
        self.assertEqual(True, simple_plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        plugin_manager.stop()

        # Make sure the plugin was stopped.
        self.assertEqual(True, simple_plugin.stopped)

    def test_start_and_stop_errors(self):
        """start and stop errors"""

        simple_plugin = SimplePlugin()
        bad_plugin = BadPlugin()
        plugin_manager = PluginManager(plugins=[simple_plugin, bad_plugin])

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        with self.assertRaises(ZeroDivisionError):
            plugin_manager.start()

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        with self.assertRaises(ZeroDivisionError):
            plugin_manager.stop()

        # Try to start a non-existent plugin.
        with self.assertRaises(ValueError):
            plugin_manager.start_plugin(plugin_id="bogus")

        # Try to stop a non-existent plugin.
        with self.assertRaises(ValueError):
            plugin_manager.stop_plugin(plugin_id="bogus")

    def test_only_include_plugins_whose_ids_are_in_the_include_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ["foo", "bar"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = PluginManager(
                include=include,
                plugins=[
                    SimplePlugin(id="foo"),
                    SimplePlugin(id="bar"),
                    SimplePlugin(id="baz"),
                ],
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["foo", "bar"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_only_include_plugins_matching_a_wildcard_in_the_include_list(
        self,
    ):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ["b*"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = PluginManager(
                include=include,
                plugins=[
                    SimplePlugin(id="foo"),
                    SimplePlugin(id="bar"),
                    SimplePlugin(id="baz"),
                ],
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["bar", "baz"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_ignore_plugins_whose_ids_are_in_the_exclude_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ["foo", "baz"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = PluginManager(
                exclude=exclude,
                plugins=[
                    SimplePlugin(id="foo"),
                    SimplePlugin(id="bar"),
                    SimplePlugin(id="baz"),
                ],
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["bar"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_ignore_plugins_matching_a_wildcard_in_the_exclude_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ["b*"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = PluginManager(
                exclude=exclude,
                plugins=[
                    SimplePlugin(id="foo"),
                    SimplePlugin(id="bar"),
                    SimplePlugin(id="baz"),
                ],
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["foo"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    #### Private protocol #####################################################

    def _test_start_and_stop(self, plugin_manager, expected):
        """
        Make sure the plugin manager starts and stops the expected plugins.
        """

        # Make sure the plugin manager found only the required plugins.
        self.assertEqual(expected, [plugin.id for plugin in plugin_manager])

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        plugin_manager.start()

        # Make sure all of the the plugins were started.
        for id in expected:
            plugin = plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        plugin_manager.stop()

        # Make sure all of the the plugins were stopped.
        for id in expected:
            plugin = plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.stopped)
