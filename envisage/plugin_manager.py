# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A simple plugin manager implementation. """


import logging

from traits.api import Event, HasTraits, Instance, List, observe, provides

from .i_application import IApplication
from .i_plugin import IPlugin
from .i_plugin_manager import IPluginManager
from .plugin_event import PluginEvent

logger = logging.getLogger(__name__)


@provides(IPluginManager)
class PluginManager(HasTraits):
    """A simple plugin manager implementation.

    This implementation manages an explicit collection of plugin instances,
    e.g::

        plugin_manager = PluginManager(plugins=[MyPlugin(), YourPlugin()])

    Plugins can be added and removed after construction time via the methods
    'add_plugin' and 'remove_plugin'.

    """

    #### 'IPluginManager' protocol ############################################

    #: Fired when a plugin has been added to the manager.
    plugin_added = Event(PluginEvent)

    #: Fired when a plugin has been removed from the manager.
    plugin_removed = Event(PluginEvent)

    #### 'PluginManager' protocol #############################################

    #: The application that the plugin manager is part of.
    application = Instance(IApplication)

    @observe("application")
    def _set_new_application_on_all_plugins(self, event):
        """Static trait change handler."""

        self._update_application_on_plugins([], self._plugins)

    #### 'object' protocol ####################################################

    def __init__(self, plugins=None, **traits):
        """Constructor.

        We allow the caller to specify an initial list of plugins, but the
        list itself is not part of the public API. To add and remove plugins
        after construction, use the 'add_plugin' and 'remove_plugin' methods
        respectively. The manager is also iterable, so to iterate over the
        plugins use 'for plugin in plugin_manager'.

        """
        super().__init__(**traits)

        if plugins is not None:
            self._plugins = plugins

    def __iter__(self):
        """Return an iterator over the manager's plugins."""

        # Iterate over a copy, so that plugins added or removed during the
        # iteration don't affect it.
        return iter(self._plugins[:])

    #### 'IPluginManager' protocol ############################################

    def add_plugin(self, plugin):
        """Add a plugin to the manager."""

        self._plugins.append(plugin)
        self.plugin_added = PluginEvent(plugin=plugin)

    def get_plugin(self, plugin_id):
        """Return the plugin with the specified Id."""

        for plugin in self._plugins:
            if plugin_id == plugin.id:
                break

        else:
            plugin = None

        return plugin

    def remove_plugin(self, plugin):
        """Remove a plugin from the manager."""

        self._plugins.remove(plugin)
        self.plugin_removed = PluginEvent(plugin=plugin)

    def start(self):
        """Start the plugin manager."""

        for plugin in self._plugins:
            self.start_plugin(plugin)

    def start_plugin(self, plugin=None, plugin_id=None):
        """Start the specified plugin."""

        plugin = plugin or self.get_plugin(plugin_id)
        if plugin is not None:
            logger.debug("plugin %s starting", plugin.id)
            plugin.activator.start_plugin(plugin)
            logger.debug("plugin %s started", plugin.id)

        else:
            raise ValueError("no such plugin %s" % plugin_id)

    def stop(self):
        """Stop the plugin manager."""

        # We stop the plugins in the reverse order that they were started.
        stop_order = self._plugins[:]
        stop_order.reverse()

        for plugin in stop_order:
            self.stop_plugin(plugin)

    def stop_plugin(self, plugin=None, plugin_id=None):
        """Stop the specified plugin."""

        plugin = plugin or self.get_plugin(plugin_id)
        if plugin is not None:
            logger.debug("plugin %s stopping", plugin.id)
            plugin.activator.stop_plugin(plugin)
            logger.debug("plugin %s stopped", plugin.id)

        else:
            raise ValueError("no such plugin %s" % plugin_id)

    #### Protected 'PluginManager' ############################################

    # The plugins that the manager manages!
    _plugins = List(IPlugin)

    @observe("_plugins")
    def _update_application_on_all_plugins(self, event):
        """Static trait change handler."""
        old, new = event.old, event.new
        self._update_application_on_plugins(old, new)

    @observe("_plugins:items")
    def _update_application_on_changed_plugins(self, event):
        """Static trait change handler."""

        self._update_application_on_plugins(event.removed, event.added)

    #### Private protocol #####################################################

    def _update_application_on_plugins(self, removed, added):
        """Update the 'application' trait of plugins added/removed."""

        for plugin in removed:
            plugin.application = None

        for plugin in added:
            plugin.application = self.application
