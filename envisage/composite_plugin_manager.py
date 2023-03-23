# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A plugin manager composed of other plugin managers! """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import (
    Event,
    HasTraits,
    Instance,
    List,
    observe,
    on_trait_change,
    provides,
)

# Local imports.
from .i_application import IApplication
from .i_plugin import IPlugin
from .i_plugin_manager import IPluginManager
from .plugin_event import PluginEvent
from .plugin_manager import PluginManager

# Logging.
logger = logging.getLogger(__name__)


@provides(IPluginManager)
class CompositePluginManager(HasTraits):
    """A plugin manager composed of other plugin managers!

    e.g::

        plugin_manager = CompositePluginManager(
             plugin_managers = [
                 EggBasketPluginManager(...),
                 PackagePluginManager(...),
             ]
        )

    """

    #### 'IPluginManager' protocol ############################################

    #### Events ####

    # Fired when a plugin has been added to the manager.
    plugin_added = Event(PluginEvent)

    # Fired when a plugin has been removed from the manager.
    plugin_removed = Event(PluginEvent)

    #### 'CompositePluginManager' protocol ####################################

    # The application that the plugin manager is part of.
    application = Instance(IApplication)

    @observe("application")
    def _update_application(self, event):
        new = event.new
        for plugin_manager in self.plugin_managers:
            plugin_manager.application = new

    # The plugin managers that make up this plugin manager!
    #
    # This is currently a list of 'PluginManager's as opposed to, the more
    # preferable 'IPluginManager' because the interface doesn't currently
    # have an 'application' trait. Should we move 'application' up to
    # 'IPluginManager'?
    plugin_managers = List(PluginManager)

    @on_trait_change("plugin_managers[]")
    def _update_application_on_plugins(self, obj, trait_named, removed, added):
        for plugin_manager in removed:
            plugin_manager.application = self.application

        for plugin_manager in added:
            plugin_manager.application = self.application

    @on_trait_change("plugin_managers:plugin_added")
    def _plugin_added(self, obj, trait_name, old, new):
        self.plugin_added = new

    @on_trait_change("plugin_managers:plugin_removed")
    def _plugin_removed(self, obj, trait_name, old, new):
        self.plugin_removed = new

    #### Private protocol #####################################################

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
        """Return an iterator over the manager's plugins."""

        plugins = []
        for plugin_manager in self.plugin_managers:
            for plugin in plugin_manager:
                plugins.append(plugin)

        return iter(plugins)

    #### 'IPluginManager' protocol ############################################

    def add_plugin(self, plugin):
        """Add a plugin to the manager."""

        raise NotImplementedError

    def get_plugin(self, plugin_id):
        """Return the plugin with the specified Id."""

        for plugin in self:
            if plugin_id == plugin.id:
                break

        else:
            plugin = None

        return plugin

    def remove_plugin(self, plugin):
        """Remove a plugin from the manager."""

        raise NotImplementedError

    def start(self):
        """Start the plugin manager."""

        for plugin in self:
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
        stop_order = list(iter(self))
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
