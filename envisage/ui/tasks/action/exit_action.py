# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# Enthought library imports.
from pyface.action.api import Action


class ExitAction(Action):
    """An action that exits the application."""

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = "Exit the application"

    # The action's name (displayed on menus/tool bar tools etc).
    name = "E&xit"

    # A short description of the action used for tooltip text etc.
    tooltip = "Exit the application"

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        event.task.window.application.exit()
