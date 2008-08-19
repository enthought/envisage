""" An action that displays the preferences dialog. """


# Enthought library imports.
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

        from enthought.preferences.ui.api import PreferencesManager
        
        # Lookup the preferences manager service.
        manager = event.window.application.get_service(PreferencesManager)
        ui = manager.edit_traits(parent=event.window.control, kind='modal')
        
        # If the UI result of the PreferencesPage was 'True', then save the preferences
        # now in case the application crashes before it exits!
        if ui.result:
            event.window.application.preferences.save()

        return

#### EOF ######################################################################
