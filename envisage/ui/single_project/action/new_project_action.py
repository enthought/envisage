""" An action that creates a new project. """

# Enthought library imports.
from envisage.ui.single_project.project_action import ProjectAction
from pyface.api import ImageResource

##############################################################################
# class 'NewProjectAction'
##############################################################################

class NewProjectAction(ProjectAction):
    """ An action that creates a new project. """

    # The universal object locator (UOL).
    uol = 'envisage.ui.single_project.ui_service.UiService'

    # The name of the method to invoke on the object.
    method_name = 'create'

    # A longer description of the action.
    description = 'Create a project'

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('new_project')

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'New...'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Create a project'
