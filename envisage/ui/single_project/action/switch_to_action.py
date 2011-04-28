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
