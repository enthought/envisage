from pyface.api import GUI, Window
from traits.api import HasTraits, Instance


class Application(HasTraits):

    gui = Instance(GUI, ())

    window = Instance(Window)

    def run(self):
        gui = self.gui
        self.window = Window()
        self.window.open()
        gui.start_event_loop()

    def exit(self):
        self.window.destroy()
        self.window.closed = True


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
