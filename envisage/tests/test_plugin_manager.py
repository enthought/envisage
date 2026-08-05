# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
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
