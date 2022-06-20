import weakref

from pyface.qt import QtCore, QtGui
from pyface.ui.qt4.gui import GUI
from traits.api import Any, Bool, HasStrictTraits, Instance


class Window(HasStrictTraits):

    #: The toolkit specific control that represents the widget.
    control = Any()

    #: The control's optional parent control.
    parent = Any()

    #: Whether or not the control is enabled
    enabled = Bool(True)

    #: The event filter for the widget.
    _event_filter = Instance(QtCore.QObject)

    def _create(self):
        """Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        self.control = self._create_control(self.parent)
        self._add_event_listeners()

    def _add_event_listeners(self):
        self.control.installEventFilter(self._event_filter)

    def _remove_event_listeners(self):
        if self._event_filter is not None:
            if self.control is not None:
                self.control.removeEventFilter(self._event_filter)
            self._event_filter = None

    def open(self):
        self._create()

    def close(self):
        self.destroy()

    def _create_control(self, parent):
        """Create a default QMainWindow."""
        control = QtGui.QMainWindow(parent)

        control.setEnabled(self.enabled)
        control.setVisible(True)

        return control

    def destroy(self):
        control = self.control
        self.control.hide()
        self.control.deleteLater()
        self._remove_event_listeners()
        self.control = None
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


class Application(HasStrictTraits):

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
