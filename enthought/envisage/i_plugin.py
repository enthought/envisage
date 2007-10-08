""" The plugin interface. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface, List, Str
from enthought.envisage.api import IApplication


class IPlugin(Interface):
    """ The plugin interface. """

    # The application that the plugin is part of.
    application = Instance(IApplication)

    # A description of what the plugin is and does.
    description = Str

    # The plugin's unique identifier.
    #
    # Where 'unique' technically means 'unique within the plugin manager', but
    # since the chances are that you will want to include plugins from external
    # sources, this really means 'globally unique'! Using the Python package
    # path might be useful here ;^)
    #
    # e.g. 'enthought.envisage'
    id = Str

    # The plugin's name (suitable for displaying to the user).
    name = Str

    # The Ids of the plugins that must be started before this one is started
    # (this is usually because this plugin requires a service that the other
    # plugin starts).
    requires = List(Str)
    
    def start(self):
        """ Start the plugin.

        Can be called manually, but is usually called exactly once when the
        application starts.

        """

    def stop(self):
        """ Stop the plugin.

        Can be called manually, but is usually called exactly once when the
        application exits.

        """

#### EOF ######################################################################
