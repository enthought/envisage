""" Tests for the plugin manager. """


# Enthought library imports.
from envisage.api import Plugin, PluginManager
from traits.api import Bool
from traits.testing.unittest_tools import unittest


class SimplePlugin(Plugin):
    """ A simple plugin. """

    #### 'SimplePlugin' interface #############################################

    started = Bool(False)
    stopped = Bool(False)

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        self.started = True
        self.stopped = False

        return

    def stop(self):
        """ Stop the plugin. """

        self.started = False
        self.stopped = True

        return


class BadPlugin(Plugin):
    """ A plugin that just causes trouble ;^). """

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        raise 1/0

    def stop(self):
        """ Stop the plugin. """

        raise 1/0


class PluginManagerTestCase(unittest.TestCase):
    """ Tests for the plugin manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_get_plugin(self):
        """ get plugin """

        simple_plugin  = SimplePlugin()
        plugin_manager = PluginManager(plugins=[simple_plugin])

        # Get the plugin.
        plugin = plugin_manager.get_plugin(simple_plugin.id)
        self.assertEqual(plugin, simple_plugin)

        # Try to get a non-existent plugin.
        self.assertEqual(None, plugin_manager.get_plugin('bogus'))

        return

    def test_iteration_over_plugins(self):
        """ iteration over plugins """

        simple_plugin = SimplePlugin()
        bad_plugin    = BadPlugin()

        plugin_manager = PluginManager(plugins=[simple_plugin, bad_plugin])

        # Iterate over the plugin manager's plugins.
        plugins = []
        for plugin in plugin_manager:
            plugins.append(plugin)

        self.assertEqual([simple_plugin, bad_plugin], plugins)

        return

    def test_start_and_stop(self):
        """ start and stop """

        simple_plugin  = SimplePlugin()
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

        return

    def test_start_and_stop_errors(self):
        """ start and stop errors """

        simple_plugin  = SimplePlugin()
        bad_plugin     = BadPlugin()
        plugin_manager = PluginManager(plugins=[simple_plugin, bad_plugin])

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        self.failUnlessRaises(ZeroDivisionError, plugin_manager.start)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        self.failUnlessRaises(ZeroDivisionError, plugin_manager.stop)

        # Try to start a non-existent plugin.
        self.failUnlessRaises(
            SystemError, plugin_manager.start_plugin, plugin_id='bogus'
        )

        # Try to stop a non-existent plugin.
        self.failUnlessRaises(
            SystemError, plugin_manager.stop_plugin, plugin_id='bogus'
        )

        return

    def test_only_include_plugins_whose_ids_are_in_the_include_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ['foo', 'bar']

        plugin_manager = PluginManager(
            include = include,
            plugins = [
                SimplePlugin(id='foo'),
                SimplePlugin(id='bar'),
                SimplePlugin(id='baz')
            ]
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['foo', 'bar']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_only_include_plugins_matching_a_wildcard_in_the_include_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ['b*']

        plugin_manager = PluginManager(
            include = include,
            plugins = [
                SimplePlugin(id='foo'),
                SimplePlugin(id='bar'),
                SimplePlugin(id='baz')
            ]
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['bar', 'baz']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_ignore_plugins_whose_ids_are_in_the_exclude_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ['foo', 'baz']

        plugin_manager = PluginManager(
            exclude = exclude,
            plugins = [
                SimplePlugin(id='foo'),
                SimplePlugin(id='bar'),
                SimplePlugin(id='baz')
            ]
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['bar']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    def test_ignore_plugins_matching_a_wildcard_in_the_exclude_list(self):

        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ['b*']

        plugin_manager = PluginManager(
            exclude = exclude,
            plugins = [
                SimplePlugin(id='foo'),
                SimplePlugin(id='bar'),
                SimplePlugin(id='baz')
            ]
        )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ['foo']

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

        return

    #### Private protocol #####################################################

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
