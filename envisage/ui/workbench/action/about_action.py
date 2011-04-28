""" An action that shows the 'About' dialog. """


# Enthought library imports.
from pyface.action.api import Action


class AboutAction(Action):
    """ An action that shows the 'About' dialog. """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Display information about the application'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'About'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Display information about the application'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        self.window.application.about()

        return

#### EOF ######################################################################
