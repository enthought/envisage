import weakref

from pyface.qt import QtCore, QtGui
from pyface.ui.qt4.gui import GUI
from pyface.ui.qt4.widget import Widget
from traits.api import HasTraits, Instance


class Window(Widget):
    """The toolkit specific implementation of a Window.  See the IWindow
    interface for the API documentation.
    """

    def open(self):
        # Create the control, if necessary.
        if self.control is None:
            self._create()

        self.show(True)
        self.opened = self

    def close(self):
        self.destroy()

    # Private interface ------------------------------------------------------

    def _create_control(self, parent):
        """Create a default QMainWindow."""
        control = QtGui.QMainWindow(parent)

        control.setEnabled(self.enabled)
        control.setVisible(self.visible)

        return control

    def destroy(self):
        if self.control is not None:
            control = self.control
            super().destroy()
            control.close()

    def __event_filter_default(self):
        return WindowEventFilter(self)


class WindowEventFilter(QtCore.QObject):
    """An internal class that watches for certain events on behalf of the
    Window instance.
    """

    def __init__(self, window):
        """Initialise the event filter."""
        QtCore.QObject.__init__(self)
        # use a weakref to fix finalization issues with circular references
        # we don't want to be the last thing holding a reference to the window
        self._window = weakref.ref(window)

    def eventFilter(self, obj, e):
        """Adds any event listeners required by the window."""

        window = self._window()
        if e.type() == QtCore.QEvent.Type.Close:
            # Do not destroy the window during its event handler.
            GUI.invoke_later(window.close)

            if window.control is not None:
                e.ignore()

            return True

        return False


class Application(HasTraits):

    window = Instance(Window)

    def run(self):
        app = QtGui.QApplication()
        self.window = Window()
        self.window.open()
        app.exec_()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
