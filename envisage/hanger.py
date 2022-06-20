from pyface.gui import GUI
from pyface.tasks.api import TaskWindow as PyfaceTaskWindow
from pyface.tasks.task_window_layout import TaskWindowLayout
from traits.api import (
    Bool,
    Callable,
    Event,
    HasStrictTraits,
    HasTraits,
    Instance,
    Int,
    List,
    Str,
    Vetoable,
)

from envisage.api import Application

class TaskWindow(PyfaceTaskWindow):
    """A TaskWindow for use with the Envisage Tasks plugin."""

    #: The application that created and is managing this window.
    application = Instance("TasksApplication")


class TaskWindowEvent(HasTraits):
    """A task window lifecycle event."""

    #: The window that the event occurred on.
    window = Instance(TaskWindow)


class VetoableTaskWindowEvent(TaskWindowEvent, Vetoable):
    """A vetoable task window lifecycle event."""

    pass


class TasksApplicationState(HasStrictTraits):
    """A class used internally by TasksApplication for saving and restoring
    application state.
    """

    # TaskWindowLayouts for the windows extant at application
    # exit. Only used if 'always_use_default_layout' is disabled.
    previous_window_layouts = List(Instance(TaskWindowLayout))

    # A list of TaskWindowLayouts accumulated throughout the application's
    # lifecycle.
    window_layouts = List(Instance(TaskWindowLayout))

    # The "version" for the state data. This should be incremented whenever a
    # backwards incompatible change is made to this class or any of the layout
    # classes. This ensures that loading application state is always safe.
    version = Int(1)

    def get_equivalent_window_layout(self, window_layout):
        """Gets an equivalent TaskWindowLayout, if there is one."""
        for layout in self.window_layouts:
            if layout.is_equivalent_to(window_layout):
                return layout
        return None

    def get_task_layout(self, task_id):
        """Gets a TaskLayout with the specified ID, there is one."""
        for window_layout in self.window_layouts:
            for layout in window_layout.items:
                if layout.id == task_id:
                    return layout
        return None

    def push_window_layout(self, window_layout):
        """Merge a TaskWindowLayout into the accumulated list."""
        self.window_layouts = [
            layout
            for layout in self.window_layouts
            if not layout.is_equivalent_to(window_layout)
        ]
        self.window_layouts.insert(0, window_layout)


class TasksApplication(Application):
    """The entry point for an Envisage Tasks application.

    This class handles the common case for Tasks applications and is
    intended to be subclassed to modify its start/stop behavior, etc.

    """

    #: Extension point ID for task factories
    TASK_FACTORIES = "envisage.ui.tasks.tasks"

    #: Extension point ID for task extensions
    TASK_EXTENSIONS = "envisage.ui.tasks.task_extensions"

    #: Pickle protocol to use for persisting layout information.
    layout_save_protocol = Int(4)

    #### 'TasksApplication' interface #########################################

    #: The active task window (the last one to get focus).
    active_window = Instance(TaskWindow)

    #: The Pyface GUI for the application.
    gui = Instance(GUI)

    #: The name of the application (also used on window title bars).
    name = Str

    #: The list of task windows created by the application.
    windows = List(Instance(TaskWindow))

    #: The factory for creating task windows.
    window_factory = Callable

    #### Application layout ###################################################

    #: The default layout for the application. If not specified, a single
    #: window will be created with the first available task factory.
    default_layout = List(Instance(TaskWindowLayout))

    #: Whether to always apply the default *application level* layout when the
    #: application is started. Even if this is True, the layout state of
    #: individual tasks will be restored.
    always_use_default_layout = Bool(False)

    #### Application lifecycle events #########################################

    #: Fired after the initial windows have been created and the GUI event loop
    #: has been started.
    application_initialized = Event

    #: Fired immediately before the extant windows are destroyed and the GUI
    #: event loop is terminated.
    application_exiting = Event

    #: Fired when a task window has been created.
    window_created = Event(Instance(TaskWindowEvent))

    #: Fired when a task window is opening.
    window_opening = Event(Instance(VetoableTaskWindowEvent))

    #: Fired when a task window has been opened.
    window_opened = Event(Instance(TaskWindowEvent))

    #: Fired when a task window is closing.
    window_closing = Event(Instance(VetoableTaskWindowEvent))

    #: Fired when a task window has been closed.
    window_closed = Event(Instance(TaskWindowEvent))

    #### Protected interface ##################################################

    # An 'explicit' exit is when the the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # Application state.
    _state = Instance(TasksApplicationState)

    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    def run(self):
        """Run the application.

        Returns
        -------
        bool
            Whether the application started successfully (i.e., without a
            veto).
        """
        gui = self.gui

        started = self.start()
        if started:
            # Create windows from the default or saved application layout.
            self._create_windows()

            # Start the GUI event loop.
            gui.set_trait_later(self, "application_initialized", self)
            print("Starting event loop")
            gui.start_event_loop()
            print("Event loop finished")

        return started

    ###########################################################################
    # 'TasksApplication' interface.
    ###########################################################################

    def create_window(self, layout=None, restore=True, **traits):
        """Creates a new TaskWindow, possibly with some Tasks.

        Parameters
        ----------
        layout : TaskWindowLayout, optional
             The layout to use for the window. The tasks described in
             the layout will be created and added to the window
             automatically. If not specified, the window will contain
             no tasks.

        restore : bool, optional (default True)
             If set, the application will restore old size and
             positions for the window and its panes, if possible. If a
             layout is not provided, this parameter has no effect.

        **traits : dict, optional
             Additional parameters to pass to ``window_factory()``
             when creating the TaskWindow.

        Returns
        -------
        envisage.ui.tasks.task_window.TaskWindow
            The new TaskWindow.

        """
        window = self.window_factory(application=self, **traits)

        # Listen for the window events.
        window.on_trait_change(self._on_window_activated, "activated")
        window.on_trait_change(self._on_window_opening, "opening")
        window.on_trait_change(self._on_window_opened, "opened")
        window.on_trait_change(self._on_window_closing, "closing")
        window.on_trait_change(self._on_window_closed, "closed")

        # Event notification.
        self.window_created = TaskWindowEvent(window=window)

        if layout:
            # Create and add tasks.
            for task_id in layout.get_tasks():
                task = self.create_task(task_id)
                window.add_task(task)

            # Apply a suitable layout.
            if restore:
                layout = self._restore_layout_from_state(layout)
        else:
            # Create an empty layout to set default size and position only
            layout = TaskWindowLayout()

        window.set_window_layout(layout)

        return window

    def exit(self, force=False):
        """Exits the application, closing all open task windows.

        Each window is sent a veto-able closing event. If any window vetoes the
        close request, no window will be closed. Otherwise, all windows will be
        closed and the GUI event loop will terminate.

        This method is not called when the user clicks the close
        button on a window or otherwise closes a window through his or
        her window manager. It is only called via the File->Exit menu
        item. It can also, of course, be called programatically.

        Parameters
        ----------
        force : bool, optional (default False)
            If set, windows will receive no closing events and will be
            destroyed unconditionally. This can be useful for reliably
            tearing down regression tests, but should be used with
            caution.

        Returns
        -------
        bool
            A boolean indicating whether the application exited.

        """
        print("Exiting")

        self._explicit_exit = True
        try:
            self._prepare_exit()
            for window in reversed(self.windows):
                window.destroy()
                window.closed = True
        finally:
            self._explicit_exit = False

        print("Successfully exited")
        return True

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _create_windows(self):
        """Called at startup to create TaskWindows from the default or saved
        application layout.
        """
        # Build a list of TaskWindowLayouts.
        self._load_state()
        if (
            self.always_use_default_layout
            or not self._state.previous_window_layouts
        ):
            window_layouts = self.default_layout
        else:
            # Choose the stored TaskWindowLayouts, but only if all the task IDs
            # are still valid.
            window_layouts = self._state.previous_window_layouts
            for layout in window_layouts:
                for task_id in layout.get_tasks():
                    if not self._get_task_factory(task_id):
                        window_layouts = self.default_layout
                        break
                else:
                    continue
                break

        # Create a TaskWindow for each TaskWindowLayout.
        for window_layout in window_layouts:
            if self.always_use_default_layout:
                window = self.create_window(window_layout, restore=False)
            else:
                window = self.create_window(window_layout, restore=True)
            window.open()

    def _prepare_exit(self):
        """Called immediately before the extant windows are destroyed and the
        GUI event loop is terminated.
        """
        print("_prepare_exit")

        self.application_exiting = self

    def _load_state(self):
        """Loads saved application state, if possible."""
        self._state = TasksApplicationState()

    def _restore_layout_from_state(self, layout):
        """Restores an equivalent layout from saved application state."""
        # First, see if a window layout matches exactly.
        match = self._state.get_equivalent_window_layout(layout)
        if match:
            # The active task is not part of the equivalency relation, so we
            # ensure that it is correct.
            match.active_task = layout.get_active_task()
            layout = match

        # If that fails, at least try to restore the layout of
        # individual tasks.
        else:
            layout = layout.clone_traits()
            for i, item in enumerate(layout.items):
                id = item if isinstance(item, str) else item.id
                match = self._state.get_task_layout(id)
                if match:
                    layout.items[i] = match

        return layout

    #### Trait initializers ###################################################

    def _window_factory_default(self):
        return TaskWindow

    def _default_layout_default(self):
        return [TaskWindowLayout()]

    def _gui_default(self):
        return GUI()

    #### Trait change handlers ################################################

    def _on_window_activated(self, window, trait_name, event):
        self.active_window = window

    def _on_window_opening(self, window, trait_name, event):
        # Event notification.
        self.window_opening = window_event = VetoableTaskWindowEvent(
            window=window
        )

        if window_event.veto:
            event.veto = True

    def _on_window_opened(self, window, trait_name, event):
        self.windows.append(window)

        # Event notification.
        self.window_opened = TaskWindowEvent(window=window)

    def _on_window_closing(self, window, trait_name, event):

        print("_on_window_closing")

        # Event notification.
        self.window_closing = window_event = VetoableTaskWindowEvent(
            window=window
        )

        if window_event.veto:
            event.veto = True
        else:
            # Store the layout of the window.
            window_layout = window.get_window_layout()
            self._state.push_window_layout(window_layout)

            # If we're exiting implicitly and this is the last window, save
            # state, because we won't get another chance.
            if len(self.windows) == 1 and not self._explicit_exit:
                self._prepare_exit()

    def _on_window_closed(self, window, trait_name, event):

        print("_on_window_closed")

        self.windows.remove(window)

        # Event notification.
        self.window_closed = TaskWindowEvent(window=window)

        # Was this the last window?
        if len(self.windows) == 0:
            print("Calling stop")
            self.stop()


def main():
    app = TasksApplication()
    app.on_trait_change(
        lambda: app.exit(force=True), "application_initialized"
    )
    print("Running application")
    app.run()
    print("Finished running appliction")


if __name__ == "__main__":
    main()
