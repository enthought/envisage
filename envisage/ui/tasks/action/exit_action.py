# Enthought library imports.
from pyface.api import ImageResource
from pyface.action.api import Action


class ExitAction(Action):
    """ An action that exits the application.
    """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Exit the application'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'E&xit'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Exit the application'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        event.task.window.application.exit()
