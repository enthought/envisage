""" The default plugin manager implementation. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Event, HasTraits, Instance, List, implements
from enthought.traits.api import on_trait_change

# Local imports.
from i_application import IApplication
from i_plugin import IPlugin
from i_plugin_manager import IPluginManager
from plugin_event import PluginEvent


# Logging.
logger = logging.getLogger(__name__)


class PluginManager(HasTraits):
    """ The default plugin manager implementation. """

    implements(IPluginManager)

    #### 'IPluginManager' interface ###########################################

    # Fired when a plugin is about to be started.
    plugin_starting = Event(PluginEvent)

    # Fired when a plugin has been started.
    plugin_started = Event(PluginEvent)

    # Fired when a plugin is about to be stopped.
    plugin_stopping = Event(PluginEvent)

    # Fired when a plugin has been stopped.
    plugin_started = Event(PluginEvent)

    #### 'PluginManager' interface ############################################

    # The application that the plugin manager is part of.
    application = Instance(IApplication)
    
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

    def start(self, plugin_context=None):
        """ Start the plugin manager.
        
        """

        map(lambda p: self.start_plugin(plugin_context, p), self.plugins)
        
        return

    def start_plugin(self, plugin_context=None, plugin=None, id=None):
        """ Start the specified plugin.

        """

        plugin = plugin or self.get_plugin(id)
        if plugin is not None:
            logger.debug('plugin %s starting', plugin.id)

            # fixme: Quick hack!!
            plugin.get_extension_points()

            self.plugin_starting = PluginEvent(plugin=plugin)
            plugin.start()
            self.plugin_started = PluginEvent(plugin=plugin)

            logger.debug('plugin %s started', plugin.id)

        else:
            raise SystemError('no such plugin %s' % id)
        
        return

    def stop(self, plugin_context=None):
        """ Stop the plugin manager.

        """

        # We stop the plugins in the reverse order that they were started.
        stop_order = self.plugins[:]
        stop_order.reverse()
        
        map(lambda p: self.stop_plugin(plugin_context, p), stop_order)

        return
    
    def stop_plugin(self, plugin_context=None, plugin=None, id=None):
        """ Stop the specified plugin.

        """

        plugin = plugin or self.get_plugin(id)
        if plugin is not None:
            logger.debug('plugin %s stopping', plugin.id)

            self.plugin_stopping = PluginEvent(plugin=plugin)
            plugin.stop()
            self.plugin_stopped = PluginEvent(plugin=plugin)

            logger.debug('plugin %s stopped', plugin.id)

        else:
            raise SystemError('no such plugin %s' % id)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(self.plugins, [])

        return

    def _plugins_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(new, old)

        return

    def _plugins_items_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(new.added, new.removed)

        return

    #### Methods ##############################################################

    def _update_plugin_application(self, added, removed):
        """ Update the 'application' trait of plugins added/removed. """

        for plugin in removed:
            plugin.application = None

        for plugin in added:
            plugin.application = self.application

        return

#### EOF ######################################################################
