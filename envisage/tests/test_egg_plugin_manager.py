# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the Egg plugin manager. """


# Enthought library imports.
from envisage.api import EggPluginManager

# Local imports.
from .test_egg_based import EggBasedTestCase
from traits.testing.unittest_tools import unittest


class EggPluginManagerTestCase(EggBasedTestCase):
    """ Tests for the Egg plugin manager. """

    ###########################################################################
    # Tests.
    ###########################################################################

    # fixme: Depending how many eggs are on sys.path, this test may take too
    # long to be part of the TDD cycle.
    def test_no_include_or_exclude(self):
        """ no include or exclude """

        # Add all of the eggs in the egg basket.
        self._add_eggs_on_path([self.egg_dir])

        # Make sure that the plugin manager only includes those plugins.
        plugin_manager = EggPluginManager()

        # We don't know how many plugins we will actually get - it depends on
        # what eggs are on sys.path! What we *do* know however is the the 3
        # 'acme' test eggs should be in there!
        ids = [plugin.id for plugin in plugin_manager]

        self.assertTrue('acme.foo' in ids)
        self.assertTrue('acme.bar' in ids)
        self.assertTrue('acme.baz' in ids)

        return

    def test_include_specific(self):
        """ include specific """
        # Add all of the eggs in the egg basket.
        self._add_eggs_on_path([self.egg_dir])

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.foo', 'acme.bar']

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ['acme\.foo', 'acme\.bar']

        # Make sure that the plugin manager only includes those plugins.
        plugin_manager = EggPluginManager(include=include)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_include_multiple(self):
        """ include multiple """

        # Add all of the eggs in the egg basket.
        self._add_eggs_on_path([self.egg_dir])

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.foo', 'acme.bar', 'acme.baz']

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ['acme.*']

        # Make sure that the plugin manager only includes those plugins.
        plugin_manager = EggPluginManager(include=include)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_exclude_specific(self):
        """ exclude specific """

        # Add all of the eggs in the egg basket.
        self._add_eggs_on_path([self.egg_dir])

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.bar']

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ['acme.*']

        # Now exclude all but 'acme.bar'...
        exclude = ['acme\.foo', 'acme\.baz']

        # Make sure that the plugin manager excludes the specified plugins.
        plugin_manager = EggPluginManager(include=include, exclude=exclude)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_exclude_multiple(self):
        """ exclude multiple """

        # Add all of the eggs in the egg basket.
        self._add_eggs_on_path([self.egg_dir])

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.foo']

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ['acme.*']

        # Now exclude every plugin that starts with 'acme.b'.
        exclude = ['acme\.b.*']

        # Make sure that the plugin manager excludes the specified plugins.
        plugin_manager = EggPluginManager(include=include, exclude=exclude)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _test_start_and_stop(self, plugin_manager, expected):
        """ Make sure the plugin manager starts and stops the expected plugins.

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

        return
