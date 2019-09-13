# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

# Enthought library imports.
from pyface.action.api import ActionItem, Group
from pyface.tasks.api import TaskWindowLayout
from pyface.tasks.action.api import TaskAction
from traits.api import List, Str

# Local imports
from envisage._compat import unicode_str


class TaskWindowLaunchAction(TaskAction):
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

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _task_changed(self, task):
        """ Name the action (unless a name has already been assigned).
        """
        if task and not self.name:
            name = unicode_str()
            for factory in task.window.application.task_factories:
                if factory.id == self.task_id:
                    name = factory.name
                    break
            self.name = name


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
            action = TaskWindowLaunchAction(task_id=factory.id)
            items.append(ActionItem(action=action))
        return items
