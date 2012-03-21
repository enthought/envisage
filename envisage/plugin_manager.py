""" A simple plugin manager implementation. """


from fnmatch import fnmatch
import logging

from traits.api import Event, HasTraits, Instance, List, Str, implements

from i_application import IApplication
from i_plugin import IPlugin
from i_plugin_manager import IPluginManager
from plugin_event import PluginEvent



logger = logging.getLogger(__name__)


class PluginManager(HasTraits):
    """ A simple plugin manager implementation.

    This implementation manages an explicit collection of plugin instances,
    e.g::

        plugin_manager = PlugunManager(
             plugins = [
                 MyPlugin(),
                 YourPlugin()
             ]
        )

    Plugins can be added and removed after construction time via the methods
    'add_plugin' and 'remove_plugin'.
    
    """

    implements(IPluginManager)

    #### 'IPluginManager' protocol #############################################

    # Fired when a plugin has been added to the manager.
    plugin_added = Event(PluginEvent)

    # Fired when a plugin has been removed from the manager.
    plugin_removed = Event(PluginEvent)

    #### 'PluginManager' protocol ##############################################

    # The application that the plugin manager is part of.
    application = Instance(IApplication)
    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application([], self._plugins)

        return

    # An optional list of the Ids of the plugins that are to be excluded by
    # the manager.
    #
    # Each item in the list is actually an 'fnmatch' expression.
    exclude = List(Str)

    # An optional list of the Ids of the plugins that are to be included by
    # the manager (i.e. *only* plugins with Ids in this list will be added to
    # the manager).
    #
    # Each item in the list is actually an 'fnmatch' expression.
    include = List(Str)

    #### 'object' protocol #####################################################

    def __init__(self, plugins=None, **traits):
        """ Constructor.

        We allow the caller to specify an initial list of plugins, but the
        list itself is not part of the public API. To add and remove plugins
        after construction, use the 'add_plugin' and 'remove_plugin' methods
        respectively. The manager is also iterable, so to iterate over the
        plugins use 'for plugin in plugin_manager'.

        """

        super(PluginManager, self).__init__(**traits)

        if plugins is not None:
            self._plugins = plugins

        return

    def __iter__(self):
        """ Return an iterator over the manager's plugins. """

        plugins = [
            plugin for plugin in self._plugins

            if self._include_plugin(plugin.id)
        ]
        
        return iter(plugins)

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
                if not self._include_plugin(plugin.id):
                    plugin = None
                    
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

    #### Protected 'PluginManager' #############################################

    # The plugins that the manager manages!
    _plugins = List(IPlugin)
    def __plugins_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(old, new)

        return

    def __plugins_items_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self._update_plugin_application(new.removed, new.added)

        return

    def _include_plugin(self, plugin_id):
        """ Return True if the plugin should be included.

        This is just shorthand for:-

        if self._is_included(plugin_id) and not self._is_excluded(plugin_id):
            ...

        """

        return self._is_included(plugin_id) and not self._is_excluded(plugin_id)
    
    #### Private protocol ######################################################

    def _is_excluded(self, plugin_id):
        """ Return True if the plugin Id is excluded.

        If no 'exclude' patterns are specified then this method returns False
        for all plugin Ids.

        """

        if len(self.exclude) == 0:
            return False

        for pattern in self.exclude:
            if fnmatch(plugin_id, pattern):
                return True

        return False

    def _is_included(self, plugin_id):
        """ Return True if the plugin Id is included.

        If no 'include' patterns are specified then this method returns True
        for all plugin Ids.

        """

        if len(self.include) == 0:
            return True

        for pattern in self.include:
            if fnmatch(plugin_id, pattern):
                return True

        return False

    def _update_plugin_application(self, removed, added):
        """ Update the 'application' trait of plugins added/removed. """

        for plugin in removed:
            plugin.application = None

        for plugin in added:
            plugin.application = self.application

        return

#### EOF ######################################################################
