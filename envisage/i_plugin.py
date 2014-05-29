""" The plugin interface. """


# Enthought library imports.
from traits.api import Instance, Interface, Str

# Local imports.
from .i_plugin_activator import IPluginActivator


class IPlugin(Interface):
    """ The plugin interface. """

    # The activator used to start and stop the plugin.
    activator = Instance(IPluginActivator)

    # The application that the plugin is part of.
    application = Instance('envisage.api.IApplication')

    # The name of a directory (created for you) that the plugin can read and
    # write to at will.
    home = Str

    # The plugin's unique identifier.
    #
    # Where 'unique' technically means 'unique within the plugin manager', but
    # since the chances are that you will want to include plugins from external
    # sources, this really means 'globally unique'! Using the Python package
    # path might be useful here. e.g. 'envisage'.
    id = Str

    # The plugin's name (suitable for displaying to the user).
    name = Str

    def start(self):
        """ Start the plugin.

        This method is called by the framework when the application is starting
        up. If you want to start a plugin manually use::

          application.start_plugin(plugin)

        """

    def stop(self):
        """ Stop the plugin.

        This method is called by the framework when the application is
        stopping. If you want to stop a plugin manually use::

          application.stop_plugin(plugin)

        """

#### EOF ######################################################################
