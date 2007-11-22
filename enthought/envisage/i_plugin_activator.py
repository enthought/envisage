""" The plugin activator interface. """


# Enthought library imports.
from enthought.traits.api import Interface


class IPluginActivator(Interface):
    """ The plugin activator interface.

    Every plugin has a plugin activator that is associated with it. The
    activator is used to start and stop the plugin. Using the activator allows
    the framework to implement default start and stop behavior, without forcing
    plugin writers to call 'super(..., self).start()' if they implement a
    custom 'start' method.

    """

    def start_plugin(self, plugin):
        """ Start the specified plugin.

        """

    def stop_plugin(self, plugin):
        """ Stop the specified plugin.

        """
        
#### EOF ######################################################################
