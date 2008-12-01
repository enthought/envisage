""" Tests for the Egg plugin manager. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import EggPluginManager

# Local imports.
from egg_based_test_case import EggBasedTestCase


# The current 'best practise' is to make the entry point name the same as
# the plugin Id. This allows us to not have to even import plugins that
# we are not interested in.
class MyEggPluginManager(EggPluginManager):
    """ An egg plugin manager that relies on entry point names being plugin Ids

    """

    ###########################################################################
    # Protected 'PluginManager' interface.
    ###########################################################################

    def __plugins_default(self):
        """ Trait initializer. """

        from enthought.envisage.egg_utils import get_entry_points_in_egg_order

        plugins = []
        for ep in get_entry_points_in_egg_order(self.working_set,self.PLUGINS):
            if len(self.include) == 0 or ep.name in self.include:
                klass  = ep.load()
                plugin = klass(application=self.application)
                plugins.append(plugin)

        return plugins

    
class EggPluginManagerTestCase(EggBasedTestCase):
    """ Tests for the Egg plugin manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        EggBasedTestCase.setUp(self)

        self.plugin_manager = MyEggPluginManager()
        
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

        # Add all of the plugin eggs to 'sys.path'.
        self._add_eggs_on_path()

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
            plugin for plugin in self.plugin_manager

            if plugin in [foo, bar, baz]
        ]
        
        self.assertEqual([foo, bar, baz], plugins)

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
