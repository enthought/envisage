""" Tests for the Egg plugin manager. """


# Enthought library imports.
from enthought.envisage.api import EggPluginManager

# Local imports.
from egg_based_test_case import EggBasedTestCase


class EggPluginManagerTestCase(EggBasedTestCase):
    """ Tests for the Egg plugin manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        EggBasedTestCase.setUp(self)
        
        self.plugin_manager = EggPluginManager()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_start_and_stop(self):
        """ start and stop """

        # The Ids of our test plugins.
        ids = ['acme.foo', 'acme.bar', 'acme.baz']

        # Make sure that the plugin manager only includes those plugins.
        self.plugin_manager.include = ids

        # Add all the plugin eggs to 'sys.path'.
        self._add_egg('acme.foo-0.1a1-py2.4.egg')
        self._add_egg('acme.bar-0.1a1-py2.4.egg')
        self._add_egg('acme.baz-0.1a1-py2.4.egg')

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        self.plugin_manager.start()
            
        # Make sure all of the the plugins were started.
        for id in ids:
            plugin = self.plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        self.plugin_manager.stop()

        # Make sure all of the the plugins were stopped.
        for id in ids:
            plugin = self.plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.stopped)

        # Make sure we got the plugins in dependency order.
        foo = self.plugin_manager.get_plugin('acme.foo')
        bar = self.plugin_manager.get_plugin('acme.bar')
        baz = self.plugin_manager.get_plugin('acme.baz')

        # Ignore any other plugins that may be in the working set.
        plugins = [
            plugin for plugin in self.plugin_manager.plugins

            if plugin in [foo, bar, baz]
        ]
        
        self.assertEqual([foo, bar, baz], plugins)

        return

#### EOF ######################################################################
