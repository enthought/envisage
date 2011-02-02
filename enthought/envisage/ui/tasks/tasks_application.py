# Standard library imports.
import logging

# Enthought library imports.
from enthought.envisage.api import Application
from enthought.pyface.api import GUI, SplashScreen
from enthought.traits.api import Bool, Callable, File, Instance, List, Str

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

    #### 'TasksApplication' interface #########################################

    # The active task window (the last one to get focus).
    active_window = Instance(TaskWindow)

    # The PyFace GUI for the application.
    gui = Instance(GUI)

    # The splash screen for the application. By default, there is no splash
    # scren.
    splash_screen = Instance(SplashScreen)

    # The directory on the local file system used to persist window layout
    # information.
    state_location = File

    # The list of task windows created by the application.
    windows = List(TaskWindow)

    # The factory for creating task windows.
    window_factory = Callable(TaskWindow)

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
            # Create and open the first task window.
            window = self.create_window()
            window.open()

            # Start the GUI event loop.
            gui.start_event_loop()

    ###########################################################################
    # 'TasksApplication' interface.
    ###########################################################################

    def create_window(self, **kw):
        """ Factory method that creates a new task window.
        """
        window = self.window_factory(application=self, **kw)

        # Listen for the window events.
        window.on_trait_change(self._on_window_activated, 'activated')
        window.on_trait_change(self._on_window_opening, 'opening')
        window.on_trait_change(self._on_window_opened, 'opened')
        window.on_trait_change(self._on_window_closing, 'closing')
        window.on_trait_change(self._on_window_closed, 'closed')

        # Event notification.
        self.window_created = TaskWindowEvent(window=window)

        return window

    def exit(self):
        """ Exits the application, closing all open task windows.

        Returns whether the application exited (whether all the windows were
        successfully closed.)

        This method is not called when the user clicks the close button or
        otherwise closes a window through his or her window manager. It is
        called only through File->Exit.
        """
        success = True
        for window in reversed(self.windows):
            if not window.close():
                success = False
                break
        return success

    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait initializers ###################################################

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

        # This is necessary because the activated event is not fired when a
        # window is first opened and gets focus. It is only fired when the
        # window comes from lower in the stack to be the active window.
        self.active_window = window

        # Event notification.
        self.window_opened = TaskWindowEvent(window=window)

    def _on_window_closing(self, window, trait_name, event):
        # Event notification.
        self.window_closing = window_event = VetoableTaskWindowEvent(
            window=window)
        
        if window_event.veto:
            event.veto = True

    def _on_window_closed(self, window, trait_name, event):
        self.windows.remove(window)

        # Event notification.
        self.window_closed = WindowEvent(window=window)

        # Was this the last window?
        if len(self.windows) == 0:
            # Invoke later to ensure that 'closed' event handlers get called
            # before 'stop()' does.
            self.gui.invoke_later(self.stop)
