# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An action that switches the project perspective. """

# Enthought library imports.
from envisage.ui.single_project.project_action import ProjectAction
from pyface.api import ImageResource


class SwitchToAction(ProjectAction):
    """ An action that switches the project perspective. """

    # A longer description of the action.
    description = 'View the current project in the Project perspective'

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('switch_project')

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Switch To Project'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Go to the Project perspective'

    def perform(self, event):
        """ Perform the action. """

        self.window.application.about()

        return
