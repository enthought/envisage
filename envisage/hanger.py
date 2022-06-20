from pyface.gui import GUI
from pyface.tasks.api import TaskWindow as PyfaceTaskWindow
from traits.api import Event, Instance

from envisage.api import Application


class TasksApplication(Application):

    gui = Instance(GUI, ())

    window = Instance(PyfaceTaskWindow)

    application_initialized = Event

    def run(self):
        """Run the application."""
        gui = self.gui

        self.start()

        self.window = PyfaceTaskWindow()
        self.window.open()

        gui.set_trait_later(self, "application_initialized", self)
        print("Starting event loop")
        gui.start_event_loop()
        print("Event loop finished")

    def exit(self):
        """Exits the application, closing all open windows."""

        print("Exiting")

        self.window.destroy()
        self.window.closed = True

        self.stop()

        print("Successfully exited")
        return True


def main():
    app = TasksApplication()
    app.on_trait_change(lambda: app.exit(), "application_initialized")
    print("Running application")
    app.run()
    print("Finished running application")


if __name__ == "__main__":
    main()
