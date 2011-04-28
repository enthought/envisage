""" A plugin event. """


# Enthought library imports.
from traits.api import Instance, Vetoable


class PluginEvent(Vetoable):
    """ A plugin event. """

    # The plugin that the event is for.
    plugin = Instance('envisage.api.IPlugin')

#### EOF ######################################################################
