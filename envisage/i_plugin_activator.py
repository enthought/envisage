""" The plugin activator interface. """


# Enthought library imports.
from traits.api import Interface


class IPluginActivator(Interface):
    """ The plugin activator interface.

    A plugin activator is really just a collection of two strategies - one
    to start the plugin and one to stop it.

    We use an activator so that the framework can implement default start and
    stop strategies without forcing the plugin writer to call 'super' if they
    override the 'start' and 'stop' methods on 'IPlugin'.

    I'm not sure that having to call 'super' is such a burden, but some people
    seem to like it this way, and it does mean one less thing for a plugin
    writer to have to remember to do!

    """

    def start_plugin(self, plugin):
        """ Start the specified plugin.

        """

    def stop_plugin(self, plugin):
        """ Stop the specified plugin.

        """

#### EOF ######################################################################
