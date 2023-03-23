# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that exits the workbench. """


from pyface.action.api import Action

# Enthought library imports.
from pyface.api import ImageResource


class ExitAction(Action):
    """An action that exits the workbench."""

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = "Exit the application"

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource("exit")

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Exit"

    # A short description of the action used for tooltip text etc.
    tooltip = "Exit the application"

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """Perform the action."""

        self.window.application.exit()
