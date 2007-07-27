""" The plugin interface. """


# Enthought library imports.
from enthought.traits.api import Interface, Str


class IPlugin(Interface):
    """ The plugin interface. """

    # The plugin's unique identifier.
    #
    # Where 'unique' technically means 'unique within the plugin manager', but
    # since you may want to include plugins from external sources, this really
    # means 'globally unique'!.
    id = Str
    
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
