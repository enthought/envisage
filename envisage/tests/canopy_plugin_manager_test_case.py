""" Tests for the Canopy plugin manager. """


import logging
from os.path import dirname, join
import unittest

from envisage.canopy_plugin_manager import CanopyPluginManager


class CanopyPluginManagerTestCase(unittest.TestCase):
    """ Tests for the Canopy plugin manager. """

    #### 'unittest.TestCase' protocol #########################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # The location of the 'eggs' directory.
        self.plugin_dir = join(dirname(__file__), 'eggs')

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return
        
    #### Tests ################################################################

    def test_finds_plugins_in_eggs(self):

        plugin_manager = CanopyPluginManager(plugin_path=[self.plugin_dir])
        ids            = [plugin.id for plugin in plugin_manager]

        self.assertEqual(len(ids), 3)
        self.assertIn('acme.foo', ids)
        self.assertIn('acme.bar', ids)
        self.assertIn('acme.baz', ids)

        return

    def test_only_finds_plugins_whose_ids_are_in_the_include_list(self):

        # Note that the items in the list are regular expressions hence you
        # need to 'escape' the '.' character if you don't want it to mean
        # 'any character'!!
        include = ['acme\.foo', 'acme\.bar']

        plugin_manager = CanopyPluginManager(
            plugin_path = [self.plugin_dir],
            include     = include
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.foo', 'acme.bar']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_only_finds_plugins_matching_a_wildcard_in_the_include_list(self):

        # Note that the items in the list are regular expressions hence you
        # need to 'escape' the '.' character if you don't want it to mean
        # 'any character'!!
        include = ['acme\.b.*']

        plugin_manager = CanopyPluginManager(
            plugin_path = [self.plugin_dir],
            include     = include
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.bar', 'acme.baz']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_ignores_plugins_whose_ids_are_in_the_exclude_list(self):

        # Note that the items in the list are regular expressions hence you
        # need to 'escape' the '.' character if you don't want it to mean
        # 'any character'!!
        exclude = ['acme\.foo', 'acme\.baz']

        plugin_manager = CanopyPluginManager(
            plugin_path = [self.plugin_dir],
            exclude     = exclude
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.bar']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_ignores_plugins_matching_a_wildcard_in_the_exclude_list(self):

        # Note that the items in the list are regular expressions hence you
        # need to 'escape' the '.' character if you don't want it to mean
        # 'any character'!!
        exclude = ['acme\.b.*']

        plugin_manager = CanopyPluginManager(
            plugin_path = [self.plugin_dir],
            exclude     = exclude
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['acme.foo']

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


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
