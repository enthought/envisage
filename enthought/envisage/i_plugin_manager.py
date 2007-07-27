""" The plugin manager interface. """


# Enthought library imports.
from enthought.traits.api import Event, Interface

# Local imports.
from plugin_event import PluginEvent


class IPluginManager(Interface):
    """ The plugin manager interface. """

    # Fired when a plugin is about to be started.
    plugin_starting = Event(PluginEvent)

    # Fired when a plugin has been started.
    plugin_started = Event(PluginEvent)

    # Fired when a plugin is about to be stopped.
    plugin_stopping = Event(PluginEvent)

    # Fired when a plugin has been stopped.
    plugin_started = Event(PluginEvent)

    def get_plugin(self, id):
        """ Return the plugin with the specified Id.

        Return None if no such plugin exists.

        """
        
    def start(self, plugin_context=None):
        """ Start the plugin manager.

        This starts all of the manager's plugins.
        
        """

    def start_plugin(self, plugin_context=None, plugin=None, id=None):
        """ Start the specified plugin.

        If a plugin is specified then start it.

        If no plugin is specified then the Id is used to look up the plugin
        and then start it. If no such plugin exists then a 'SystemError'
        exception is raised.

        """

    def stop(self, plugin_context=None):
        """ Stop the plugin manager.

        This stop's all of the plugin manager's plugins (in the reverse order
        that they were started).

        """

    def stop_plugin(self, plugin_context=None, plugin=None, id=None):
        """ Stop the specified plugin.

        If a plugin is specified then stop it (the Id is ignored).

        If no plugin is specified then the Id is used to look up the plugin and
        then stop it. If no such plugin exists then a 'SystemError' exception
        is raised.

        """
        
#### EOF ######################################################################
