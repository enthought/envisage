# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An action to close the current project.  This is only enabled when
    there is a current project.
"""

# Enthought library imports
from envisage.ui.single_project.project_action import ProjectAction
from pyface.api import ImageResource

##############################################################################
# class 'CloseProjectAction'
##############################################################################


class CloseProjectAction(ProjectAction):
    """ An action to close the current project.  This is only enabled when
        there is a current project.
    """

    # The universal object locator (UOL).
    uol = "envisage.ui.single_project.ui_service.UiService"

    # The name of the method to invoke on the object.
    method_name = "close"

    # A longer description of the action.
    description = "Close the current project"

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource("close_project")

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Close"

    # A short description of the action used for tooltip text etc.
    tooltip = "Close this project"
