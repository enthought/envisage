# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the 'Package' plugin manager. """


from os.path import dirname, join

from envisage.package_plugin_manager import PackagePluginManager
from traits.testing.unittest_tools import unittest


class PackagePluginManagerTestCase(unittest.TestCase):
    """ Tests for the 'Package' plugin manager. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # The location of the 'plugins' test data directory.
        self.plugins_dir = join(dirname(__file__), 'plugins')

    def test_find_plugins_in_packages_on_the_plugin_path(self):

        plugin_manager = PackagePluginManager(plugin_path=[self.plugins_dir])
        ids            = [plugin.id for plugin in plugin_manager]

        self.assertEqual(len(ids), 3)
        self.assertIn('banana', ids)
        self.assertIn('orange', ids)
        self.assertIn('pear', ids)

    def test_only_find_plugins_whose_ids_are_in_the_include_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ['orange', 'pear']

        plugin_manager = PackagePluginManager(
            plugin_path = [self.plugins_dir],
            include     = include
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['orange', 'pear']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_only_find_plugins_matching_a_wildcard_in_the_include_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ['*r*']

        plugin_manager = PackagePluginManager(
            plugin_path = [self.plugins_dir],
            include     = include
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['orange', 'pear']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_ignore_plugins_whose_ids_are_in_the_exclude_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ['orange', 'pear']

        plugin_manager = PackagePluginManager(
            plugin_path = [self.plugins_dir],
            exclude     = exclude
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['banana']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_ignore_plugins_matching_a_wildcard_in_the_exclude_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ['*r*']

        plugin_manager = PackagePluginManager(
            plugin_path = [self.plugins_dir],
            exclude     = exclude
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['banana']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_reflect_changes_to_the_plugin_path(self):
        plugin_manager = PackagePluginManager()
        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 0)

        plugin_manager.plugin_path.append(self.plugins_dir)
        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 3)
        self.assertIn('banana', ids)
        self.assertIn('orange', ids)
        self.assertIn('pear', ids)

        del plugin_manager.plugin_path[0]
        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 0)

    #### Private protocol #####################################################

    def _test_start_and_stop(self, plugin_manager, expected):
        """ Make sure the plugin manager starts and stops the expected plugins.

        """

        # Make sure the plugin manager found only the required plugins.
        self.assertEqual(
            list(sorted(expected)),
            list(sorted(plugin.id for plugin in plugin_manager))
        )

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
