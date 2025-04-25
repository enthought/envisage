# (C) Copyright 2007-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A view containing a colored panel! """


from pyface.workbench.api import View

# Enthought library imports.
from traits.etsconfig.api import ETSConfig

_TOOLKIT_MAPPING = {
    "qt4": "qt",
}


def _normalize_toolkit_name(toolkit):
    """Convert legacy toolkit names to current toolkit names."""

    toolkit = toolkit.lower()
    return _TOOLKIT_MAPPING.get(toolkit, toolkit)


class ColorView(View):
    """A view containing a colored panel!

    This view is written so that it works with *both* wx and Qt4. Your own
    views obviously do not have to do this!

    """

    #### 'IView' interface ####################################################

    # The category that the view belongs to.
    category = "Color"

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _id_default(self):
        """Trait initializer."""

        # By making the Id the same as the name, we make it easy to specify
        # the views in the example perspectives. Note for larger applications
        # the Id should be globally unique, and by default we use the module
        # name and class name.
        return self.name

    #### Methods ##############################################################

    def create_control(self, parent):
        """Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        toolkit = _normalize_toolkit_name(ETSConfig.toolkit)
        method = getattr(self, f"_{toolkit}_create_control", None)
        if method is None:
            raise RuntimeError(f"Unknown toolkit {ETSConfig.toolkit}")

        color = self.name.lower()

        return method(parent, color)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _wx_create_control(self, parent, color):
        """Create a wx version of the control."""

        import wx

        panel = wx.Panel(parent, -1)
        panel.SetBackgroundColour(color)

        return panel

    def _qt_create_control(self, parent, color):
        """Create a Qt version of the control."""

        from pyface.qt import QtGui

        widget = QtGui.QWidget(parent)

        palette = widget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

        return widget
