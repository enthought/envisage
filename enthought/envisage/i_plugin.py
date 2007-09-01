""" The plugin interface. """


# Enthought library imports.
from enthought.traits.api import Interface, List, Str


class IPlugin(Interface):
    """ The plugin interface. """

    # The plugin's unique identifier.
    #
    # Where 'unique' technically means 'unique within the plugin manager', but
    # since you may want to include plugins from external sources, this really
    # means 'globally unique'!.
    id = Str

    # The plugin's name (suitable for displaying to the user).
    name = Str

    # A description of what the plugin is and does.
    description = Str

    # The Ids of the plugins that must be started before this one is started
    # (this is usually because this plugin requires a service that the other
    # plugin starts).
    requires = List(Str)
    
    def start(self, plugin_context):
        """ Start the plugin.

        Can be called manually, but is usually called exactly once when the
        application starts.

        """

    def stop(self, plugin_context):
        """ Stop the plugin.

        Can be called manually, but is usually called exactly once when the
        application exits.

        """

#### EOF ######################################################################
