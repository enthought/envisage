""" Tests for the Egg plugin manager. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import EggPluginManager

# Local imports.
from egg_based_test_case import EggBasedTestCase

    
class EggPluginManagerTestCase(EggBasedTestCase):
    """ Tests for the Egg plugin manager. """

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_start_and_stop(self):
        """ start and stop """

        # Add all of the eggs in the egg basket.
        self._add_eggs_on_path([self.egg_dir])
        
        # The Ids of our test plugins.
        ids = ['acme.foo', 'acme.bar', 'acme.baz']

        # Make sure that the plugin manager only includes those plugins.
        plugin_manager = EggPluginManager(include=ids)

        # Make sure the plugin manager found only the required plugins.
        self.assertEqual(ids, [plugin.id for plugin in plugin_manager])

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        plugin_manager.start()
            
        # Make sure all of the the plugins were started.
        for id in ids:
            plugin = plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        plugin_manager.stop()

        # Make sure all of the the plugins were stopped.
        for id in ids:
            plugin = plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.stopped)

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
