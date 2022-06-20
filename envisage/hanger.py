from pyface.api import GUI, ApplicationWindow
from traits.api import Event, HasTraits, Instance


class Application(HasTraits):

    gui = Instance(GUI, ())

    window = Instance(ApplicationWindow)

    application_initialized = Event

    def run(self):
        gui = self.gui

        self.window = ApplicationWindow()
        self.window.open()

        gui.set_trait_later(self, "application_initialized", self)
        gui.start_event_loop()

    def exit(self):
        self.window.destroy()
        self.window.closed = True


def main():
    app = Application()
    app.on_trait_change(lambda: app.exit(), "application_initialized")
    app.run()


if __name__ == "__main__":
    main()
