""" The plugin interface. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface, List, Str


class IPlugin(Interface):
    """ The plugin interface. """

    # The application that the plugin is part of.
    application = Instance('enthought.envisage.api.IApplication')

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

        This method is called by the framework exactly once when the
        application is starting up. If you want to start a plugin manually call
        'application.start_plugin'.

        """

    def stop(self):
        """ Stop the plugin.

        This method is called by the framework exactly once when the
        application is stopping. If you want to stop a plugin manually call
        'application.stop_plugin'.

        """

#### EOF ######################################################################
