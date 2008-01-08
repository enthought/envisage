""" The plotting plugin. """


# Enthought library imports.
from enthought.envisage import Plugin
from enthought.traits.api import Instance

# Plugin definition imports.
from plot_data_manager import PlotDataManager
from plot_template_manager import PlotTemplateManager
from plotting_plugin_definition import PlotDataFactories, PlotTemplateFactories

class PltPlugin(Plugin):
    """ The plt plugin. """

    # The shared plugin instance.
    instance = None

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **kw):
        """ Creates a new plugin. """

        # Base class constructor.
        super(PltPlugin, self).__init__(**kw)

        # Set the shared instance.
        PltPlugin.instance = self

        return

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def start(self, application):
        """ Starts the plugin. """

        pass

    def stop(self, application):
        """ Stops the plugin. """

        pass


#### EOF ######################################################################
