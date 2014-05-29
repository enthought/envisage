# Enthought library imports.
from pyface.action.api import Action, ActionItem, Group
from traits.api import Any, Bool, Instance, List, Property, Unicode, \
     on_trait_change


class TaskWindowToggleAction(Action):
    """ An action for activating an application window.
    """

    #### 'Action' interface ###################################################

    name = Property(Unicode, depends_on='window.active_task.name')
    style = 'toggle'

    #### 'TaskWindowToggleAction' interface ###################################

    # The window to use for this action.
    window = Instance('envisage.ui.tasks.task_window.TaskWindow')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event=None):
        if self.window:
            self.window.activate()

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_name(self):
        if self.window.active_task:
            return self.window.active_task.name
        return unicode() if sys.version_info[0] < 3 else str()

    @on_trait_change('window:activated')
    def _window_activated(self):
        self.checked = True

    @on_trait_change('window:deactivated')
    def _window_deactivated(self):
        self.checked = False


class TaskWindowToggleGroup(Group):
    """ A Group for toggling the activation state of an application's windows.
    """

    #### 'Group' interface ####################################################

    id = 'TaskWindowToggleGroup'
    items = List

    #### 'TaskWindowToggleGroup' interface ####################################

    # The application that contains the group.
    application = Instance('envisage.ui.tasks.tasks_application.'
                           'TasksApplication')

    # The ActionManager to which the group belongs.
    manager = Any

    ###########################################################################
    # 'Group' interface.
    ###########################################################################

    def destroy(self):
        """ Called when the group is no longer required.
        """
        super(TaskWindowToggleGroup, self).destroy()
        if self.application:
            self.application.on_trait_change(
                self._rebuild, 'window_opened, window_closed', remove=True)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_items(self):
        items = []
        for window in self.application.windows:
            active = window == self.application.active_window
            action = TaskWindowToggleAction(window=window, checked=active)
            items.append(ActionItem(action=action))
        return items

    def _rebuild(self):
        # Clear out the old group, then build the new one.
        for item in self.items:
            item.destroy()
        self.items = self._get_items()

        # Inform our manager that it needs to be rebuilt.
        self.manager.changed = True

    #### Trait initializers ###################################################

    def _application_default(self):
        return self.manager.controller.task.window.application

    def _items_default(self):
        self.application.on_trait_change(self._rebuild,
                                         'window_opened, window_closed')
        return self._get_items()

    def _manager_default(self):
        manager = self
        while isinstance(manager, Group):
            manager = manager.parent
        return manager
