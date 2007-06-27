""" An application event. """


# Enthought library imports.
from enthought.traits.api import Instance, Vetoable


class ApplicationEvent(Vetoable):
    """ An application event. """

    # The application that the event is for.
    application = Instance('enthought.envisage3.api.IApplication')

#### EOF ######################################################################
