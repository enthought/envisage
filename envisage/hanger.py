try:
    from PySide6 import QtCore
    from PySide6.QtWidgets import QApplication, QMainWindow
except ImportError:
    from PySide2 import QtCore
    from PySide2.QtWidgets import QApplication, QMainWindow


class WindowEventFilter(QtCore.QObject):

    close_later = QtCore.Signal()

    def __init__(self, window):
        QtCore.QObject.__init__(self)
        self._window = window

    def eventFilter(self, obj, e):
        window = self._window
        if e.type() != QtCore.QEvent.Type.Close:
            return False

        self.close_later.emit()
        if window._control is not None:
            e.ignore()
        return True


class Window:
    def __init__(self):
        self._control = None
        self._event_filter = None

    def _add_event_listeners(self):
        event_filter = WindowEventFilter(self)
        self._event_filter = event_filter
        self._control.installEventFilter(event_filter)
        self._event_filter.close_later.connect(
            self.close, QtCore.Qt.QueuedConnection)

    def _remove_event_listeners(self):
        self._control.removeEventFilter(self._event_filter)
        self._event_filter = None

    def open(self):
        control = QMainWindow()
        control.setEnabled(True)
        control.setVisible(True)
        self._control = control
        self._add_event_listeners()

    def close(self):
        self._remove_event_listeners()
        control = self._control
        control.hide()
        control.deleteLater()
        self._control = None
        control.close()


def main():
    app = QApplication()
    window = Window()
    window.open()
    app.exec_()


if __name__ == "__main__":
    main()
