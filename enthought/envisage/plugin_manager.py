""" The default plugin manager implementation. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Any, Event, HasTraits, List, implements

# Local imports.
from i_plugin import IPlugin
from i_plugin_manager import IPluginManager
from plugin_event import PluginEvent


# Logging.
logger = logging.getLogger(__name__)


class PluginManager(HasTraits):
    """ The default plugin manager implementation. """

    implements(IPluginManager)

    #### 'IPluginManager' interface ###########################################

    # The application that the plugin manager belongs to.
    application = Any

    # Fired when a plugin is about to be started.
    plugin_starting = Event(PluginEvent)

    # Fired when a plugin has been started.
    plugin_started = Event(PluginEvent)

    # Fired when a plugin is about to be stopped.
    plugin_stopping = Event(PluginEvent)

    # Fired when a plugin has been stopped.
    plugin_started = Event(PluginEvent)

    #### 'PluginManager' interface ############################################

    # The manager's plugins.
    plugins = List(IPlugin)
    
    ###########################################################################
    # 'IPluginManager' interface.
    ###########################################################################

    def get_plugin(self, id):
        """ Return the plugin with the specified Id.

        """

        for plugin in self.plugins:
            if id == plugin.id:
                break

        else:
            plugin = None

        return plugin

    def start(self):
        """ Start the plugin manager.
        
        """

        map(self.start_plugin, self.plugins)
        
        return

    def start_plugin(self, plugin=None, id=None):
        """ Start the specified plugin.

        """

        plugin = plugin or self.get_plugin(id)
        if plugin is not None:
            try:
                logger.debug('plugin %s starting', plugin.id)

                self.plugin_starting = PluginEvent(plugin=plugin)
                plugin.start(self.application)
                self.plugin_started = PluginEvent(plugin=plugin)

                logger.debug('plugin %s started', plugin.id)
                
            except:
                logger.exception('error starting plugin %s', plugin.id)

        else:
            raise SystemError('no such plugin %s' % id)
        
        return

    def stop(self):
        """ Stop the plugin manager.

        """

        # We stop the plugins in the reverse order that they were started.
        stop_order = self.plugins[:]
        stop_order.reverse()
        
        map(self.stop_plugin, stop_order)

        return
    
    def stop_plugin(self, plugin=None, id=None):
        """ Stop the specified plugin.

        """

        plugin = plugin or self.get_plugin(id)
        if plugin is not None:
            try:
                logger.debug('plugin %s stopping', plugin.id)

                self.plugin_stopping = PluginEvent(plugin=plugin)
                plugin.stop(self.application)
                self.plugin_stopped = PluginEvent(plugin=plugin)

                logger.debug('plugin %s stopped', plugin.id)
                
            except:
                logger.exception('error stopping plugin %s', plugin.id)

        else:
            raise SystemError('no such plugin %s' % id)

        return
    
#### EOF ######################################################################
