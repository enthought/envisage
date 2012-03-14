""" A plugin manager composed of other plugin managers! """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import Event, HasTraits, Instance, List, implements
from traits.api import on_trait_change

# Local imports.
from i_application import IApplication
from i_plugin import IPlugin
from i_plugin_manager import IPluginManager
from plugin_event import PluginEvent
from plugin_manager import PluginManager


# Logging.
logger = logging.getLogger(__name__)


class CompositePluginManager(HasTraits):
    """ A plugin manager composed of other plugin managers!

    e.g::

        plugin_manager = CompositePluginManager(
             plugin_mangers = [
                 EggBasketPluginManager(...),
                 PackagePluginManager(...),
             ]
        )

    """

    implements(IPluginManager)

    #### 'IPluginManager' protocol #############################################

    #### Events ####

    # Fired when a plugin has been added to the manager.
    plugin_added = Event(PluginEvent)

    # Fired when a plugin has been removed from the manager.
    plugin_removed = Event(PluginEvent)

    #### 'CompositePluginManager' protocol #####################################

    # The application that the plugin manager is part of.
    application = Instance(IApplication)

    # The plugin managers that make up this plugin manager!
    plugin_managers = List(IPluginManager)
    @on_trait_change('plugin_managers[]')
    def _update_application(self, obj, trait_named, removed, added):
        # smell: 'IPlugin' does not currently have an 'application' trait, but
        # 'PluginManager' does! Should we move 'application' up to 'IPlugin'.
        # Otherwise, the trait definition 'List(IPlugin)' is misleading
        # because we assume an 'application' trait. Of course, Python being
        # Python this will work but the intent is unclear.
        for plugin_manager in removed:
            plugin_manager.application = self.application

        for plugin_manager in added:
            plugin_manager.application = self.application

    @on_trait_change('plugin_managers:plugin_added')
    def _plugin_added(self, obj, trait_name, old, new):
        self.plugin_added = new

    @on_trait_change('plugin_managers:plugin_removed')
    def _plugin_removed(self, obj, trait_name, old, new):
        self.plugin_removed = new
        
    #### Private protocol ######################################################

    # The plugins that the manager manages!
    _plugins = List(IPlugin)
    def __plugins_default(self):
        plugins = []
        for plugin_manager in self.plugin_managers:
            for plugin in plugin_manager:
                plugins.append(plugin)

        return plugins

    #### 'object' protocol ####################################################

    def __iter__(self):
        """ Return an iterator over the manager's plugins. """

        return iter(self._plugins)

    #### 'IPluginManager' protocol #############################################

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
            plugin.activator.start_plugin(plugin)
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
            plugin.activator.stop_plugin(plugin)
            logger.debug('plugin %s stopped', plugin.id)

        else:
            raise SystemError('no such plugin %s' % plugin_id)

        return

    #### 'PluginManager' protocol #############################################

    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        for plugin_manager in self.plugin_managers:
            plugin_manager.application = new

        return

#### EOF ######################################################################
