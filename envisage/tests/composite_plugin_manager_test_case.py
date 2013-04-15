""" Tests for the composite plugin manager. """


from envisage.application import Application
from envisage.composite_plugin_manager import CompositePluginManager
from envisage.plugin_manager import PluginManager
from envisage.plugin import Plugin
from traits.api import Bool
from traits.testing.unittest_tools import unittest


class SimplePlugin(Plugin):
    """ A simple plugin. """

    #### 'SimplePlugin' protocol ###############################################

    started = Bool(False)
    stopped = Bool(False)

    #### 'IPlugin' protocol ###################################################

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


class CompositePluginManagerTestCase(unittest.TestCase):
    """ Tests for the composite plugin manager. """

    #### 'unittest.TestCase' protocol #########################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return
        
    #### Tests ################################################################

    def test_find_no_plugins_if_there_are_no_plugin_managers(self):

        plugin_manager = CompositePluginManager()
        ids            = [plugin.id for plugin in plugin_manager]

        self.assertEqual(0, len(ids))

        return

    def test_find_no_plugins_if_there_are_no_plugins_in_plugin_managers(self):

        plugin_manager = CompositePluginManager(
            plugin_managers=[PluginManager(), PluginManager()]
        )
        ids            = [plugin.id for plugin in plugin_manager]

        self.assertEqual(0, len(ids))

        return

    def test_find_plugins_in_a_single_plugin_manager(self):

        plugin_manager = CompositePluginManager(
            plugin_managers=[
                PluginManager(
                    plugins=[SimplePlugin(id='red'), SimplePlugin(id='yellow')]
                )
            ]
        )
        ids            = [plugin.id for plugin in plugin_manager]

        self.assertEqual(2, len(ids))
        self.assertIn('red', ids)
        self.assertIn('yellow', ids)

        self._test_start_and_stop(plugin_manager, ['red', 'yellow'])
        
        return

    def test_find_plugins_in_a_multiple_plugin_managers(self):

        plugin_manager = CompositePluginManager(
            plugin_managers=[
                PluginManager(
                    plugins=[SimplePlugin(id='red'), SimplePlugin(id='yellow')]
                ),
                
                PluginManager(
                    plugins=[SimplePlugin(id='green')]
                )
            ]
        )
        ids            = [plugin.id for plugin in plugin_manager]

        self.assertEqual(3, len(ids))
        self.assertIn('red', ids)
        self.assertIn('yellow', ids)
        self.assertIn('green', ids)

        self._test_start_and_stop(plugin_manager, ['red', 'yellow', 'green'])
        
        return

    def test_application_gets_propogated_to_plugin_managers(self):

        application = Application()
        
        composite_plugin_manager = CompositePluginManager(
            application     = application,
            plugin_managers = [PluginManager(), PluginManager()]
        )

        for plugin_manager in composite_plugin_manager.plugin_managers:
            self.assertEqual(application, plugin_manager.application)

        return

    def test_propogate_plugin_added_or_remove_events_from_plugin_managers(self):

        a = PluginManager()
        b = PluginManager()
        
        composite_plugin_manager = CompositePluginManager(
            plugin_managers = [a, b]
        )
        composite_plugin_manager._plugins
        
        def added(obj, trait_name, old, new):
            added.count += 1
        added.count = 0

        composite_plugin_manager.on_trait_change(added, 'plugin_added')

        def removed(obj, trait_name, old, new):
            removed.count += 1
        removed.count = 0

        composite_plugin_manager.on_trait_change(removed, 'plugin_removed')

        a.add_plugin(Plugin(id='foo'))
        self.assertEqual(1, self._plugin_count(composite_plugin_manager))
                         
        a.remove_plugin(a.get_plugin('foo'))
        self.assertEqual(0, self._plugin_count(composite_plugin_manager))
        
        return
    
    #### Private protocol #####################################################

    def _plugin_count(self, plugin_manager):
        """ Return how many plugins the plugin manager contains. """

        count = 0
        for plugin in plugin_manager:
            count += 1

        return count
            
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
