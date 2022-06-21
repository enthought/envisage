import weakref

from pyface.qt import QtCore, QtGui
from pyface.ui.qt4.gui import GUI


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

            if window._control is not None:
                e.ignore()

            return True

        return False


class Window:
    def __init__(self):
        self._control = None
        self._event_filter = None

    def _add_event_listeners(self):
        event_filter = WindowEventFilter(self)
        self._event_filter = event_filter
        self._control.installEventFilter(event_filter)

    def _remove_event_listeners(self):
        self._control.removeEventFilter(self._event_filter)
        self._event_filter = None

    def open(self):
        control = QtGui.QMainWindow()
        control.setEnabled(True)
        control.setVisible(True)
        self._control = control
        self._add_event_listeners()

    def close(self):
        control = self._control
        control.hide()
        control.deleteLater()
        self._remove_event_listeners()
        self._control = None
        control.close()


class Application:
    def __init__(self):
        self.window = None

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
