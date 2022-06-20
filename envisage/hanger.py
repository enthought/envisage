import weakref

from pyface.qt import QtCore, QtGui
from pyface.qt.QtCore import Qt
from pyface.ui.qt4.gui import GUI
from traits.api import Any, Bool, HasTraits, Instance, Interface, Str


class MWidget(HasTraits):
    """The mixin class that contains common code for toolkit specific
    implementations of the IWidget interface.
    """

    def create(self):
        """Creates the toolkit specific control.

        The default implementation simply calls _create()
        """
        self._create()

    def destroy(self):
        """Call clean-up code and destroy toolkit objects.

        Subclasses should override to perform any additional clean-up, ensuring
        that they call super() after that clean-up.
        """
        if self.control is not None:
            self._remove_event_listeners()
            self.control = None

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create(self):
        """Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        self.control = self._create_control(self.parent)
        self._initialize_control()
        self._add_event_listeners()

    def _create_control(self, parent):
        """Create toolkit specific control that represents the widget.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control to be used as the parent for the widget's
            control.

        Returns
        -------
        control : toolkit control
            A control for the widget.
        """
        raise NotImplementedError()

    def _initialize_control(self):
        """Perform any post-creation initialization for the control."""
        pass

    def _add_event_listeners(self):
        """Set up toolkit-specific bindings for events"""
        pass

    def _remove_event_listeners(self):
        """Remove toolkit-specific bindings for events"""
        pass


class Widget(MWidget, HasTraits):
    """The toolkit specific implementation of a Widget.  See the IWidget
    interface for the API documentation.
    """

    #: The toolkit specific control that represents the widget.
    control = Any()

    #: The control's optional parent control.
    parent = Any()

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)

    #: A tooltip for the widget.
    tooltip = Str()

    #: The event filter for the widget.
    _event_filter = Instance(QtCore.QObject)

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        """Show or hide the widget.

        Parameter
        ---------
        visible : bool
            Visible should be ``True`` if the widget should be shown.
        """
        self.visible = visible
        if self.control is not None:
            self.control.setVisible(visible)

    def destroy(self):
        if self.control is not None:
            self.control.hide()
            self.control.deleteLater()
            super().destroy()

    def _add_event_listeners(self):
        super()._add_event_listeners()
        self.control.installEventFilter(self._event_filter)

    def _remove_event_listeners(self):
        if self._event_filter is not None:
            if self.control is not None:
                self.control.removeEventFilter(self._event_filter)
            self._event_filter = None
        super()._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_tooltip(self):
        """Toolkit specific method to get the control's tooltip."""
        return self.control.toolTip()

    def _set_control_tooltip(self, tooltip):
        """Toolkit specific method to set the control's tooltip."""
        self.control.setToolTip(tooltip)

    # Trait change handlers --------------------------------------------------

    def _visible_changed(self, new):
        if self.control is not None:
            self.show(new)


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
