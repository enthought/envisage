# Enthought library imports.
from enthought.pyface.action.api import Action


class PreferencesAction(Action):
    """ An action that displays the preferences dialog.
    """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Open the preferences dialog'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Preferences...'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open the preferences dialog'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        from enthought.envisage.ui.tasks.preferences_dialog import \
            PreferencesDialog

        window = event.task.window
        dialog = window.application.get_service(PreferencesDialog)
        ui = dialog.edit_traits(parent=window.control, kind='modal')
        
        if ui.result:
            window.application.preferences.save()
