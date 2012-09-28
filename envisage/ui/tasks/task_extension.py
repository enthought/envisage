# Enthought library imports.
from pyface.tasks.action.api import SchemaAddition
from traits.api import HasStrictTraits, Callable, List, Str


class TaskExtension(HasStrictTraits):
    """ A bundle of items for extending a Task.
    """

    # The ID of the task to extend. If the ID is omitted, the extension applies
    # to all tasks.
    task_id = Str

    # A list of menu bar and tool bar items to add to the set provided
    # by the task.
    actions = List(SchemaAddition)

    # A list of dock pane factories that will extend the dock panes provided by
    # the task.
    dock_pane_factories = List(Callable)
