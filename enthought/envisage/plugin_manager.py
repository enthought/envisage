""" The default plugin manager implementation. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Event, HasTraits, Instance, List, implements

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

    #### Events ####

    # Fired when a plugin has been added to the manager.
    plugin_added = Event(PluginEvent)
    
    # Fired when a plugin has been removed from the manager.
    plugin_removed = Event(PluginEvent)

    #### 'PluginManager' interface ############################################

    # The application that the plugin manager is part of.
    application = Instance(IApplication)

    #### Private interface ####################################################

    # The plugins that the manager manages!
    _plugins = List(IPlugin)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, plugins=None, **traits):
        """ Constructor. """

        super(PluginManager, self).__init__(**traits)

        # We allow the caller to specify an initial list of plugins, but the
        # list itself is not part of the public API. To add and remove plugins
        # after construction, use the 'add_plugin' and 'remove_plugin' methods
        # respectively. The manager is also iterable, so to iterate over the
        # plugins use 'for plugin in plugin_manager'.
        if plugins is not None:
            self._plugins = plugins

        return

    def __iter__(self):
        """ Return an iterator over the manager's plugins. """

        return iter(self._plugins)
    
    ###########################################################################
    # 'IPluginManager' interface.
    ###########################################################################

    def add_plugin(self, plugin):
        """ Add a plugin to the manager. """

        self._plugins.append(plugin)
        self.plugin_added = PluginEvent(plugin=plugin)

        return
    
    def get_plugin(self, plugin_id):
        """ Return the plugin with the specified Id. """

        for plugin in self._plugins:
            if plugin_id == plugin.id:
                break

        else:
            plugin = None

        return plugin
    
    def remove_plugin(self, plugin):
        """ Remove a plugin from the manager. """

        self._plugins.remove(plugin)
        self.plugin_removed = PluginEvent(plugin=plugin)

        return
    
    def start(self):
        """ Start the plugin manager. """

        map(lambda plugin: self.start_plugin(plugin), self._plugins)
        
        return

    def start_plugin(self, plugin=None, plugin_id=None):
        """ Start the specified plugin. """

        plugin = plugin or self.get_plugin(plugin_id)
        if plugin is not None:
            logger.debug('plugin %s starting', plugin.id)
            type(plugin).start_plugin(plugin)
            logger.debug('plugin %s started', plugin.id)

        else:
            raise SystemError('no such plugin %s' % plugin_id)
        
        return

    def stop(self):
        """ Stop the plugin manager. """

        # We stop the plugins in the reverse order that they were started.
        stop_order = self._plugins[:]
        stop_order.reverse()
        
        map(lambda plugin: self.stop_plugin(plugin), stop_order)

        return
    
    def stop_plugin(self, plugin=None, plugin_id=None):
        """ Stop the specified plugin. """

        plugin = plugin or self.get_plugin(plugin_id)
        if plugin is not None:
            logger.debug('plugin %s stopping', plugin.id)
            type(plugin).stop_plugin(plugin)
            logger.debug('plugin %s stopped', plugin.id)

        else:
            raise SystemError('no such plugin %s' % plugin_id)

        return
        
    ###########################################################################
    # 'PluginManager' interface.
    ###########################################################################

    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application([], self._plugins)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def __plugins_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(old, new)

        return

    def __plugins_items_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(new.removed, new.added)

        return

    #### Methods ##############################################################

    def _update_plugin_application(self, removed, added):
        """ Update the 'application' trait of plugins added/removed. """

        for plugin in removed:
            plugin.application = None

        for plugin in added:
            plugin.application = self.application

        return

#### EOF ######################################################################
