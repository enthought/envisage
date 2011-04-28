""" An action that exits the workbench. """


# Enthought library imports.
from pyface.api import ImageResource
from pyface.action.api import Action


class ExitAction(Action):
    """ An action that exits the workbench. """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Exit the application'

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('exit')

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Exit'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Exit the application'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        self.window.application.exit()

        return

#### EOF ######################################################################
