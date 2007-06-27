""" Tests for the plugin manager. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Plugin, PluginManager
from enthought.traits.api import Bool


class PluginManagerTestCase(unittest.TestCase):
    """ Tests for the plugin manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.plugin_manager = PluginManager()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_get_plugin(self):
        """ get plugin """

        plugin = Plugin()
        self.plugin_manager.plugins = [plugin]

        # Get the plugin.
        self.assertEqual(plugin, self.plugin_manager.get_plugin(plugin.id))

        # Try to get a non-existent plugin.
        self.assertEqual(None, self.plugin_manager.get_plugin('bogus'))

        return
    
    def test_start_and_stop(self):
        """ start and stop """

        class SimplePlugin(Plugin):
            """ A simple plugin. """

            #### 'SimplePlugin' interface #####################################

            started = Bool(False)
            stopped = Bool(False)
            
            ###################################################################
            # 'IPlugin' interface.
            ###################################################################

            def start(self, application):
                """ Start the plugin. """

                self.started = True
                self.stopped = False

                return

            def stop(self, application):
                """ Stop the plugin. """

                self.started = False
                self.stopped = True

                return

        simple_plugin = SimplePlugin()
        self.plugin_manager.plugins = [simple_plugin]

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        self.plugin_manager.start()

        # Make sure the plugin was started.
        self.assertEqual(True, simple_plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        self.plugin_manager.stop()

        # Make sure the plugin was stopped.
        self.assertEqual(True, simple_plugin.stopped)

        return

    def test_start_and_stop_errors(self):
        """ start and stop errors """

        class SimplePlugin(Plugin):
            """ A simple plugin. """

            #### 'SimplePlugin' interface #####################################

            started = Bool(False)
            stopped = Bool(False)
            
            ###################################################################
            # 'IPlugin' interface.
            ###################################################################

            def start(self, application):
                """ Start the plugin. """

                self.started = True
                self.stopped = False

                return

            def stop(self, application):
                """ Stop the plugin. """

                self.started = False
                self.stopped = True

                return

        class BadPlugin(Plugin):
            """ A plugin that just causes trouble ;^). """
            
            ###################################################################
            # 'IPlugin' interface.
            ###################################################################

            def start(self, application):
                """ Start the plugin. """

                raise 1/0

            def stop(self, application):
                """ Stop the plugin. """

                raise 1/0

        simple_plugin = SimplePlugin()
        bad_plugin = BadPlugin()
        self.plugin_manager.plugins = [simple_plugin, bad_plugin]

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        self.plugin_manager.start()
 
        # Make sure the plugin was started despite the bad one failing.
        self.assertEqual(True, simple_plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        self.plugin_manager.stop()

        # Make sure the plugin was stopped despite the bad one failing.
        self.assertEqual(True, simple_plugin.stopped)

        # Try to start a non-existent plugin.
        self.failUnlessRaises(
            SystemError, self.plugin_manager.start_plugin, id='bogus'
        )

        # Try to stop a non-existent plugin.
        self.failUnlessRaises(
            SystemError, self.plugin_manager.stop_plugin, id='bogus'
        )

        return

#### EOF ######################################################################
