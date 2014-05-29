""" The plugin manager interface. """


# Enthought library imports.
from traits.api import Event, Interface

# Local imports.
from .plugin_event import PluginEvent


class IPluginManager(Interface):
    """ The plugin manager interface. """

    #### Events ####

    # Fired when a plugin has been added to the manager.
    plugin_added = Event(PluginEvent)

    # Fired when a plugin has been removed from the manager.
    plugin_removed = Event(PluginEvent)

    def __iter__(self):
        """ Return an iterator over the manager's plugins.

        """

    def add_plugin(self, plugin):
        """ Add a plugin to the manager.

        """

    def get_plugin(self, plugin_id):
        """ Return the plugin with the specified Id.

        Return None if no such plugin exists.

        """

    def remove_plugin(self, plugin):
        """ Remove a plugin from the manager.

        """

    def start(self):
        """ Start the plugin manager.

        This starts all of the manager's plugins.

        """

    def start_plugin(self, plugin=None, plugin_id=None):
        """ Start the specified plugin.

        If a plugin is specified then start it.

        If no plugin is specified then the Id is used to look up the plugin
        and then start it. If no such plugin exists then a 'SystemError'
        exception is raised.

        """

    def stop(self):
        """ Stop the plugin manager.

        This stop's all of the plugin manager's plugins (in the reverse order
        that they were started).

        """

    def stop_plugin(self, plugin=None, plugin_id=None):
        """ Stop the specified plugin.

        If a plugin is specified then stop it (the Id is ignored).

        If no plugin is specified then the Id is used to look up the plugin and
        then stop it. If no such plugin exists then a 'SystemError' exception
        is raised.

        """

#### EOF ######################################################################
