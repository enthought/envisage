""" An action that opens a project. """

# Enthought library imports.
from envisage.ui.single_project.project_action import ProjectAction
from pyface.api import ImageResource

##############################################################################
# class 'OpenProjectAction'
##############################################################################

class OpenProjectAction(ProjectAction):
    """ An action that opens a project. """

    # The universal object locator (UOL).
    uol = 'envisage.ui.single_project.ui_service.UiService'

    # The name of the method to invoke on the object.
    method_name = 'open'

    # A longer description of the action.
    description = 'Open an existing project'

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('open_project')

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Open...'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open a project'
