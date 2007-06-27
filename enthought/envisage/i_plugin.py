""" The plugin interface. """


# Enthought library imports.
from enthought.traits.api import Interface, Str


class IPlugin(Interface):
    """ The plugin interface. """

    # The plugin's unique identifier.
    #
    # Where 'unique' technically means 'unique within the application', but
    # since your application may want to include plugins from external sources,
    # this really means 'globally unique'!.
    id = Str
    
    def start(self, application):
        """ Start the plugin.

        Can be called manually, but is usually called exactly once when the
        application starts.

        """

    def stop(self, application):
        """ Stop the plugin.

        Can be called manually, but is usually called exactly once when the
        application exits.

        """

#### EOF ######################################################################
