""" An application event. """


# Enthought library imports.
from traits.api import Instance, Vetoable


class ApplicationEvent(Vetoable):
    """ An application event. """

    # The application that the event is for.
    application = Instance('envisage.api.IApplication')

#### EOF ######################################################################
