# Standard library imports.
import cPickle
import logging
import os.path

# Enthought library imports.
from envisage.api import Application, ExtensionPoint
from pyface.api import GUI, SplashScreen
from pyface.image_resource import ImageResource
from pyface.tasks.api import TaskLayout, TaskWindowLayout
from traits.api import Bool, Callable, Directory, Event, HasStrictTraits, \
     Instance, Int, List, Property, Str, Unicode, Vetoable
from traits.etsconfig.api import ETSConfig

# Local imports
from task_window import TaskWindow
from task_window_event import TaskWindowEvent, VetoableTaskWindowEvent

# Logging.
logger = logging.getLogger(__name__)


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

    # Icon for the whole application. Will be used to override all taskWindows 
    # icons to have the same.
    icon = Instance(ImageResource, allow_none=True) #Any

    # The name of the application (also used on window title bars).
    name = Unicode

    # The splash screen for the application. By default, there is no splash
    # screen.
    splash_screen = Instance(SplashScreen)

    # The directory on the local file system used to persist window layout
    # information.
    state_location = Directory

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

    #### Application lifecycle events #########################################

    # Fired after the initial windows have been created and the GUI event loop
    # has been started.
    application_initialized = Event

    # Fired immediately before the extant windows are destroyed and the GUI
    # event loop is terminated.
    application_exiting = Event

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
    _state = Instance('envisage.ui.tasks.tasks_application.'
                      'TasksApplicationState')

    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    def run(self):
        """ Run the application.

        Returns:
        --------
        Whether the application started successfully (i.e., without a veto).
        """
        # Make sure the GUI has been created (so that, if required, the splash
        # screen is shown).
        gui = self.gui

        started = self.start()
        if started:
            # Create windows from the default or saved application layout.
            self._create_windows()

            # Start the GUI event loop.
            gui.set_trait_later(self, 'application_initialized', self)
            gui.start_event_loop()

        return started

    ###########################################################################
    # 'TasksApplication' interface.
    ###########################################################################

    def create_task(self, id):
        """ Creates the Task with the specified ID.

        Returns:
        --------
        The new Task, or None if there is not a suitable TaskFactory.
        """
        # Get the factory for the task.
        factory = self._get_task_factory(id)
        if factory is None:
            return None

        # Create the task using suitable task extensions.
        extensions = [ ext for ext in self.task_extensions
                       if ext.task_id == id or not ext.task_id ]
        task = factory.create_with_extensions(extensions)
        task.id = factory.id
        return task

    def create_window(self, layout=None, restore=True, **traits):
        """ Creates a new TaskWindow, possibly with some Tasks.

        Parameters:
        -----------
        layout : TaskWindowLayout, optional
             The layout to use for the window. The tasks described in the layout
             will be created and added to the window automatically. If not
             specified, the window will contain no tasks.

        restore : bool, optional (default True)
             If set, the application will restore old size and positions for the
             window and its panes, if possible. If a layout is not provided,
             this parameter has no effect.

        **traits : dict, optional
             Additional parameters to pass to ``window_factory()`` when creating
             the TaskWindow.

        Returns:
        --------
        The new TaskWindow.
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

        if layout:
            # Create and add tasks.
            for task_id in layout.get_tasks():
                task = self.create_task(task_id)
                if task:
                    window.add_task(task)
                else:
                    logger.error('Missing factory for task with ID %r', task_id)

            # Apply a suitable layout.
            if restore:
                layout = self._restore_layout_from_state(layout)
            window.set_window_layout(layout)

        return window

    def exit(self, force=False):
        """ Exits the application, closing all open task windows.

        Each window is sent a veto-able closing event. If any window vetoes the
        close request, no window will be closed. Otherwise, all windows will be
        closed and the GUI event loop will terminate.

        This method is not called when the user clicks the close button on a
        window or otherwise closes a window through his or her window
        manager. It is only called via the File->Exit menu item. It can also, of
        course, be called programatically.

        Parameters:
        -----------
        force : bool, optional (default False)
            If set, windows will receive no closing events and will be destroyed
            unconditionally. This can be useful for reliably tearing down
            regression tests, but should be used with caution.

        Returns:
        --------
        A boolean indicating whether the application exited.
        """
        self._explicit_exit = True
        try:
            if not force:
                for window in reversed(self.windows):
                    window.closing = event = Vetoable()
                    if event.veto:
                        return False

            self._prepare_exit()
            for window in reversed(self.windows):
                window.destroy()
                window.closed = True
        finally:
            self._explicit_exit = False
        return True

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _create_windows(self):
        """ Called at startup to create TaskWindows from the default or saved
            application layout.
        """
        # Build a list of TaskWindowLayouts.
        self._load_state()
        if self.always_use_default_layout or \
               not self._state.previous_window_layouts:
            window_layouts = self.default_layout
        else:
            # Choose the stored TaskWindowLayouts, but only if all the task IDs
            # are still valid.
            window_layouts = self._state.previous_window_layouts
            for layout in window_layouts:
                for task_id in layout.get_tasks():
                    if not self._get_task_factory(task_id):
                        logger.warning('Saved application layout references '
                                       'non-existent task %r. Falling back to '
                                       'default application layout.' % task_id)
                        window_layouts = self.default_layout
                        break
                else:
                    continue
                break

        # Create a TaskWindow for each TaskWindowLayout.
        for window_layout in window_layouts:
            window = self.create_window(window_layout,
                                        restore=self.always_use_default_layout)
            window.open()

    def _get_task_factory(self, id):
        """ Returns the TaskFactory with the specified ID, or None.
        """
        for factory in self.task_factories:
            if factory.id == id:
                return factory
        return None

    def _prepare_exit(self):
        """ Called immediately before the extant windows are destroyed and the
            GUI event loop is terminated.
        """
        self.application_exiting = self
        self._save_state()

    def _load_state(self):
        """ Loads saved application state, if possible.
        """
        state = TasksApplicationState()
        filename = os.path.join(self.state_location, 'application_memento')
        if os.path.exists(filename):
            # Attempt to unpickle the saved application state.
            try:
                with open(filename, 'r') as f:
                    restored_state = cPickle.load(f)
                if state.version == restored_state.version:
                    state = restored_state
                else:
                    logger.warn('Discarding outdated application layout')
            except:
                # If anything goes wrong, log the error and continue.
                logger.exception('Restoring application layout from %s',
                                 filename)
        self._state = state

    def _restore_layout_from_state(self, layout):
        """ Restores an equivalent layout from saved application state.
        """
        # First, see if a window layout matches exactly.
        match = self._state.get_equivalent_window_layout(layout)
        if match:
            # The active task is not part of the equivalency relation, so we
            # ensure that it is correct.
            match.active_task = layout.get_active_task()
            layout = match
            
        # If that fails, at least try to restore the layout of individual tasks.
        else:
            layout = layout.clone_traits()
            for i, item in enumerate(layout.items):
                id = item if isinstance(item, basestring) else item.id
                match = self._state.get_task_layout(id)
                if match:
                    layout.items[i] = match

        return layout

    def _save_state(self):
        """ Saves the application state.
        """
        # Grab the current window layouts.
        window_layouts = [ w.get_window_layout() for w in self.windows ]
        self._state.previous_window_layouts = window_layouts

        # Attempt to pickle the application state.
        filename = os.path.join(self.state_location, 'application_memento')
        try:
            with open(filename, 'w') as f:
                cPickle.dump(self._state, f)
        except:
            # If anything goes wrong, log the error and continue.
            logger.exception('Saving application layout')

    #### Trait initializers ###################################################

    def _default_layout_default(self):
        window_layout = TaskWindowLayout()
        if self.task_factories:
            window_layout.items = [ self.task_factories[0].id ]
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
            # Store the layout of the window.
            window_layout = window.get_window_layout()
            self._state.push_window_layout(window_layout)

            # If we're exiting implicitly and this is the last window, save
            # state, because we won't get another chance.
            if len(self.windows) == 1 and not self._explicit_exit:
                self._prepare_exit()

    def _on_window_closed(self, window, trait_name, event):
        self.windows.remove(window)

        # Event notification.
        self.window_closed = TaskWindowEvent(window=window)

        # Was this the last window?
        if len(self.windows) == 0:
            self.stop()


class TasksApplicationState(HasStrictTraits):
    """ A class used internally by TasksApplication for saving and restoring
        application state.
    """

    # TaskWindowLayouts for the windows extant at application exit. Only used if
    # 'always_use_default_layout' is disabled.
    previous_window_layouts = List(TaskWindowLayout)

    # A list of TaskWindowLayouts accumulated throughout the application's
    # lifecycle.
    window_layouts = List(TaskWindowLayout)

    # The "version" for the state data. This should be incremented whenever a
    # backwards incompatible change is made to this class or any of the layout
    # classes. This ensures that loading application state is always safe.
    version = Int(1)

    def get_equivalent_window_layout(self, window_layout):
        """ Gets an equivalent TaskWindowLayout, if there is one.
        """
        for layout in self.window_layouts:
            if layout.is_equivalent_to(window_layout):
                return layout
        return None

    def get_task_layout(self, task_id):
        """ Gets a TaskLayout with the specified ID, there is one.
        """
        for window_layout in self.window_layouts:
            for layout in window_layout.items:
                if layout.id == task_id:
                    return layout
        return None

    def push_window_layout(self, window_layout):
        """ Merge a TaskWindowLayout into the accumulated list.
        """
        self.window_layouts = [ layout for layout in self.window_layouts
                                if not layout.is_equivalent_to(window_layout) ]
        self.window_layouts.insert(0, window_layout)
