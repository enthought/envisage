""" Tests for the plugin manager. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Plugin, PluginManager
from enthought.traits.api import Bool


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

    def test_get_plugins(self):
        """ get plugins """

        simple_plugin  = SimplePlugin()
        plugin_manager = PluginManager(plugins=[simple_plugin])

        # Get the plugin.
        plugins = plugin_manager.get_plugins()
        self.assertEqual([simple_plugin], plugins)

        # Mess with the list.
        plugins.append(BadPlugin())

        # Make sure we didn't affect the plugin manager.
        plugins = plugin_manager.get_plugins()
        self.assertEqual([simple_plugin], plugins)

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

#### EOF ######################################################################
