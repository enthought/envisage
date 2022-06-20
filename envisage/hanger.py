from pyface.api import Window
from pyface.qt import QtGui
from traits.api import HasTraits, Instance


class Application(HasTraits):

    window = Instance(Window)

    def run(self):
        self.window = Window()
        self.window.open()
        app = QtGui.QApplication.instance()
        app.exec_()

    def exit(self):
        self.window.destroy()
        self.window.closed = True


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
