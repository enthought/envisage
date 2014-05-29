# Enthought library imports.
from traits.api import HasTraits, Instance, Vetoable

# Local imports.
from .task_window import TaskWindow


class TaskWindowEvent(HasTraits):
    """ A task window lifecycle event.
    """

    # The window that the event occurred on.
    window = Instance(TaskWindow)


class VetoableTaskWindowEvent(TaskWindowEvent, Vetoable):
    """ A vetoable task window lifecycle event.
    """

    pass
