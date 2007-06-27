""" A plugin event. """


# Enthought library imports.
from enthought.traits.api import Instance, Vetoable


class PluginEvent(Vetoable):
    """ A plugin event. """

    # The plugin that the event is for.
    plugin = Instance('enthought.envisage.api.IPlugin')

#### EOF ######################################################################
