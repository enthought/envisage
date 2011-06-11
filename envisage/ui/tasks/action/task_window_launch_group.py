# Enthought library imports.
from pyface.action.api import Action, ActionItem, Group
from pyface.tasks.api import TaskWindowLayout
from traits.api import List, Str


class TaskWindowLaunchAction(Action):
    """ An Action that creates a task window with a single task.
    """

    #### 'TaskWindowLaunchAction' interface ###################################

    task_id = Str

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        application = event.task.window.application
        window = application.create_window(TaskWindowLayout(self.task_id))
        window.open()
        

class TaskWindowLaunchGroup(Group):
    """ A Group for creating task windows with a single task.
    """

    #### 'Group' interface ####################################################

    id = 'TaskWindowLaunchGroup'
    items = List

    ###########################################################################
    # Private interface.
    ###########################################################################
    
    def _items_default(self):
        manager = self
        while isinstance(manager, Group):
            manager = manager.parent
        application = manager.controller.task.window.application

        items = []
        for factory in application.task_factories:
            action = TaskWindowLaunchAction(name=factory.name,
                                            task_id=factory.id)
            items.append(ActionItem(action=action))
        return items
