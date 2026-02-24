# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" An action that dynamically creates and adds a view. """


# Enthought library imports.
from pyface.action.api import Action
from pyface.workbench.api import View


class NewViewAction(Action):
    """An action that dynamically creates and adds a view."""

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = "Create and add a new view"

    # The action's name (displayed on menus/tool bar tools etc).
    name = "New View"

    # A short description of the action used for tooltip text etc.
    tooltip = "Create and add a new view"

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """Perform the action."""

        # You can give the view a position... (it default to 'left')...
        view = View(id="my.view.fred", name="Fred", position="right")
        self.window.add_view(view)

        # or you can specify it on the call to 'add_view'...
        view = View(id="my.view.wilma", name="Wilma")
        self.window.add_view(view, position="top")

        return
