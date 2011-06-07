# Standard library imports.
import cPickle
import logging
import os.path

# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from envisage.api import Application, ExtensionPoint
from pyface.api import GUI, SplashScreen
from pyface.tasks.api import TaskLayout, TaskWindowLayout
from traits.api import Bool, Callable, Dict, Event, File, \
    HasStrictTraits, Instance, List, Property, Str, Unicode

# Local imports
from task_window import TaskWindow
from task_window_event import TaskWindowEvent, VetoableTaskWindowEvent

# Logging.
logger = logging.getLogger(__name__)


class TasksApplicationState(HasStrictTraits):
    """ A class used internally by TasksApplication for saving and restoring
        application state.
    """

    # A mapping from task IDs to task layouts.
    task_layouts = Dict(Str, Instance(TaskLayout))

    # If 'always_use_default_layout' is set, a list of layouts accumulated
    # throughout the application's lifecycle. Otherwise, the layouts for the
    # windows extant at application exit.
    window_layouts = List(TaskWindowLayout)


class TasksApplication(Application):
    """ The entry point for an Envisage Tasks application.

    This class handles the common case for Tasks applications and is intended to
    be subclassed to modify its start/stop behavior, etc.
    """

    # Extension point IDs.
    TASK_FACTORIES  = 'envisage.ui.tasks.tasks'
    TASK_EXTENSIONS = 'envisage.ui.tasks.task_extensions'

    #### 'TasksApplication' interface #########################################

    # The active task window (the last one to get focus).
    active_window = Instance(TaskWindow)

    # The PyFace GUI for the application.
    gui = Instance(GUI)

    # The name of the application (also used on window title bars).
    name = Unicode

    # The splash screen for the application. By default, there is no splash
    # screen.
    splash_screen = Instance(SplashScreen)

    # The directory on the local file system used to persist window layout
    # information.
    state_location = File

    # Contributed task factories. This attribute is primarily for run-time
    # inspection; to instantiate a task, use the 'create_task' method.
    task_factories = ExtensionPoint(id=TASK_FACTORIES)

    # Contributed task extensions.
    task_extensions = ExtensionPoint(id=TASK_EXTENSIONS)

    # The list of task windows created by the application.
    windows = List(TaskWindow)

    # The factory for creating task windows.
    window_factory = Callable(TaskWindow)

    #### Application layout ###################################################

    # The default layout for the application. If not specified, a single window
    # will be created with the first available task factory.
    default_layout = List(TaskWindowLayout)

    # Whether to always apply the default *application level* layout when the
    # application is started. Even if this is False, the layout state of
    # individual tasks will be restored.
    always_use_default_layout = Bool(False)

    #### Window lifecycle events ##############################################

    # Fired when a task window has been created.
    window_created = Event(TaskWindowEvent)

    # Fired when a task window is opening.
    window_opening = Event(VetoableTaskWindowEvent)

    # Fired when a task window has been opened.
    window_opened = Event(TaskWindowEvent)

    # Fired when a task window is closing.
    window_closing = Event(VetoableTaskWindowEvent)

    # Fired when a task window has been closed.
    window_closed = Event(TaskWindowEvent)

    #### Protected interface ##################################################

    # An 'explicit' exit is when the the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # Application state.
    _state = Instance(TasksApplicationState, ())

    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    def run(self):
        """ Run the application.
        """
        # Make sure the GUI has been created (so that, if required, the splash
        # screen is shown).
        gui = self.gui

        if self.start():
            # Create windows from the default or saved application layout.
            self._create_windows()

            # Start the GUI event loop.
            gui.invoke_later(self.initialized)
            gui.start_event_loop()

    ###########################################################################
    # 'TasksApplication' interface.
    ###########################################################################

    def create_task(self, id):
        """ Creates the Task with the specified ID. Returns None if there is no
            suitable TaskFactory.
        """
        # Get the factory for the task.
        for factory in self.task_factories:
            if factory.id == id:
                break
        else:
            logger.error('No factory for task with id %r', id)
            return None

        # Create the task using suitable task extensions.
        extensions = [ ext for ext in self.task_extensions
                       if ext.task_id == id or not ext.task_id ]
        task = factory.create_with_extensions(extensions)
        task.id = factory.id
        return task

    def create_window(self, *ids, **traits):
        """ Creates a new TaskWindow and attaches it to the application.
        """
        window = self.window_factory(application=self, **traits)

        # Listen for the window events.
        window.on_trait_change(self._on_window_activated, 'activated')
        window.on_trait_change(self._on_window_opening, 'opening')
        window.on_trait_change(self._on_window_opened, 'opened')
        window.on_trait_change(self._on_window_closing, 'closing')
        window.on_trait_change(self._on_window_closed, 'closed')

        # Event notification.
        self.window_created = TaskWindowEvent(window=window)

        # Create tasks.
        for task_id in ids:
            task = self.create_task(task_id)
            if task:
                window.add_task(task)

        return window

    def initialized(self):
        """ Called after the windows have been created at start time.

        Implement this method to perform any final initialization after the
        event loop has been started.
        """
        pass

    def exit(self):
        """ Exits the application, closing all open task windows.

        Returns whether the application exited (whether all the windows were
        successfully closed.)

        This method is not called when the user clicks the close button or
        otherwise closes a window through his or her window manager. It is
        called only through File->Exit.
        """
        self._explicit_exit = True
        try:
            # Fetch the window layouts *before* closing the windows. If we
            # succeed in closing all the windows, we will write these to disk.
            if not self.always_use_default_layout:
                window_layouts = [ w.get_window_layout() for w in self.windows ]

            # Attempt to close all open windows.
            success = True
            for window in reversed(self.windows):
                if not window.close():
                    success = False
                    break

            # Save the state, if necesssary.
            if success:
                if not self.always_use_default_layout:
                    self._state.window_layouts = window_layouts
                self._save_state()
        finally:
            self._explicit_exit = False
        return success

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _create_windows(self):
        """ Called at startup to create TaskWindows from the default or saved
            application layout.
        """
        # Build a list of TaskWindowLayouts.
        restored_state = self._load_state()
        if self.always_use_default_layout:
            # For each window layout in the default layout, restore the maximum
            # amount of UI state possible. First, try to find an equivalent
            # saved window layout. If that fails, at least try to restore the
            # layouts of individual tasks.
            window_layouts = []
            for layout in self.default_layout:
                for restored_layout in restored_state.window_layouts:
                    if layout.is_equivalent_to(restored_layout):
                        window_layouts.append(restored_layout)
                        break
                else:
                    layout.layout_state.update(restored_state.task_layouts)
                    window_layouts.append(layout)
        else:
            if restored_state.window_layouts:
                window_layouts = restored_state.window_layouts
            else:
                window_layouts = self.default_layout

        # Create a TaskWindow for each TaskWindowLayout.
        for window_layout in window_layouts:
            window = self.create_window(*window_layout.tasks)
            window.set_window_layout(window_layout)
            window.open()

    def _load_state(self):
        """ Loads saved application state, if possible.
        """
        state = TasksApplicationState()
        filename = os.path.join(self.state_location, 'application_memento')
        if os.path.exists(filename):
            # Attempt to unpickle the saved application layout.
            try:
                with open(filename, 'r') as f:
                    state = cPickle.load(f)
            except:
                # If anything goes wrong, log the error and continue.
                logger.exception('Restoring application layout from %s',
                                 filename)
        return state

    def _save_state(self):
        """ Saves the specified application state.
        """
        filename = os.path.join(self.state_location, 'application_memento')
        with open(filename, 'w') as f:
            cPickle.dump(self._state, f)

    #### Trait initializers ###################################################

    def _default_layout_default(self):
        window_layout = TaskWindowLayout()
        if self.task_factories:
            window_layout.tasks = [ self.task_factories[0].id ]
        return [ window_layout ]

    def _gui_default(self):
        return GUI(splash_screen=self.splash_screen)

    def _state_location_default(self):
        state_location = os.path.join(ETSConfig.application_home,
                                      'tasks', ETSConfig.toolkit)
        if not os.path.exists(state_location):
            os.makedirs(state_location)

        logger.debug('Tasks state location is %s', state_location)

        return state_location

    #### Trait change handlers ################################################

    def _on_window_activated(self, window, trait_name, event):
        logger.debug('Task window %s activated', window)
        self.active_window = window

    def _on_window_opening(self, window, trait_name, event):
        # Event notification.
        self.window_opening = window_event = VetoableTaskWindowEvent(
            window=window)

        if window_event.veto:
            event.veto = True

    def _on_window_opened(self, window, trait_name, event):
        self.windows.append(window)

        # Event notification.
        self.window_opened = TaskWindowEvent(window=window)

    def _on_window_closing(self, window, trait_name, event):
        # Event notification.
        self.window_closing = window_event = VetoableTaskWindowEvent(
            window=window)

        if window_event.veto:
            event.veto = True
        else:
            # Store the layouts for the window.
            window_layout = window.get_window_layout()
            self._state.task_layouts.update(window_layout.layout_state)
            if self.always_use_default_layout:
                self._state.window_layouts.insert(0, window_layout)

            # If we're exiting implicitly and this is the last window, save
            # state, because we won't get another chance.
            if len(self.windows) == 1 and not self._explicit_exit:
                if not self.always_use_default_layout:
                    self._state.window_layouts = [ window_layout ]
                self._save_state()

    def _on_window_closed(self, window, trait_name, event):
        self.windows.remove(window)

        # Event notification.
        self.window_closed = TaskWindowEvent(window=window)

        # Was this the last window?
        if len(self.windows) == 0:
            # Invoke later to ensure that 'closed' event handlers get called
            # before 'stop()' does.
            self.gui.invoke_later(self.stop)
