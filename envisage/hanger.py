from pyface.gui import GUI
from pyface.tasks.api import TaskWindow as PyfaceTaskWindow
from pyface.tasks.task_window_layout import TaskWindowLayout
from traits.api import Event, Instance, List

from envisage.api import Application


class TasksApplication(Application):

    #: The Pyface GUI for the application.
    gui = Instance(GUI)

    #: The list of task windows created by the application.
    windows = List(Instance(PyfaceTaskWindow))

    #: Fired after the initial windows have been created and the GUI event loop
    #: has been started.
    application_initialized = Event

    def run(self):
        """Run the application."""
        gui = self.gui

        self.start()
        # Create windows from the default or saved application layout.
        self._create_windows()

        # Start the GUI event loop.
        gui.set_trait_later(self, "application_initialized", self)
        print("Starting event loop")
        gui.start_event_loop()
        print("Event loop finished")

    def exit(self, force=False):
        """Exits the application, closing all open windows."""

        print("Exiting")

        for window in reversed(self.windows):
            window.destroy()
            window.closed = True

        print("Successfully exited")
        return True

    def create_window(self, layout=None):
        window = PyfaceTaskWindow()

        # Listen for the window events.
        window.on_trait_change(self._on_window_opened, "opened")
        window.on_trait_change(self._on_window_closed, "closed")
        window.set_window_layout(layout)
        return window

    def _create_windows(self):
        """Called at startup to create TaskWindows from the default or saved
        application layout.
        """
        # Build a list of TaskWindowLayouts.
        window_layouts = [TaskWindowLayout()]

        # Create a TaskWindow for each TaskWindowLayout.
        for window_layout in window_layouts:
            window = self.create_window(window_layout)
            window.open()

    # --- Trait defaults and handlers

    def _gui_default(self):
        return GUI()

    def _on_window_opened(self, window, trait_name, event):
        self.windows.append(window)

    def _on_window_closed(self, window, trait_name, event):
        self.windows.remove(window)
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
    print("Finished running application")


if __name__ == "__main__":
    main()
