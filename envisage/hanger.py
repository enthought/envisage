import weakref

from pyface.i_window import MWindow
from pyface.qt import QtCore, QtGui
from pyface.ui.qt4.gui import GUI
from pyface.ui.qt4.widget import Widget
from traits.api import (
    Enum,
    Event,
    HasTraits,
    Instance,
    Property,
    Str,
    Tuple,
    VetoableEvent,
)


class Window(MWindow, Widget):
    """The toolkit specific implementation of a Window.  See the IWindow
    interface for the API documentation.
    """

    # Window Events ----------------------------------------------------------

    #: The window has been closed.
    closed = Event()

    #: The window is about to be closed.
    closing = VetoableEvent()

    # Private interface ------------------------------------------------------

    def _create_control(self, parent):
        """Create a default QMainWindow."""
        control = QtGui.QMainWindow(parent)

        control.setEnabled(self.enabled)

        # XXX starting with visible true is not recommended
        control.setVisible(self.visible)

        return control

    # -------------------------------------------------------------------------
    # 'IWidget' interface.
    # -------------------------------------------------------------------------

    def destroy(self):

        if self.control is not None:
            control = self.control
            super().destroy()
            control.close()

    # -------------------------------------------------------------------------
    # Private interface.
    # -------------------------------------------------------------------------

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

        # Sanity check.
        if window is None or obj is not window.control:
            return False

        typ = e.type()

        if typ == QtCore.QEvent.Type.Close:
            # Do not destroy the window during its event handler.
            GUI.invoke_later(window.close)

            if window.control is not None:
                e.ignore()

            return True

        if typ in {QtCore.QEvent.Type.Show, QtCore.QEvent.Type.Hide}:
            window.visible = window.control.isVisible()

        return False


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
