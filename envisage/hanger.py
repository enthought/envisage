from pyface.qt import QtGui
from pyface.ui.qt4.window import Window
from traits.api import HasTraits, Instance


class Application(HasTraits):

    window = Instance(Window)

    def run(self):
        app = QtGui.QApplication()
        self.window = Window()
        self.window.open()
        app.exec_()

    def exit(self):
        self.window.destroy()
        self.window.closed = True


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
