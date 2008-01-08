""" An action that displays the preferences dialog. """


# Enthought library imports.
from enthought.envisage.ui.workbench.api import WorkbenchPreferencesManager
from enthought.pyface.api import ImageResource
from enthought.pyface.action.api import Action


class EditPreferencesAction(Action):
    """ An action that displays the preferences dialog. """

    #### 'Action' interface ###################################################
    
    # A longer description of the action.
    description = 'Manage Preferences'

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('preferences')

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Preferences'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Manage Preferences'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """

        manager = WorkbenchPreferencesManager()
        manager.edit_traits(parent=event.window.control, kind='modal')

        return

#### EOF ######################################################################
