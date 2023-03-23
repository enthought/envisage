# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that displays the preferences dialog. """


from pyface.action.api import Action

# Enthought library imports.
from pyface.api import ImageResource


class EditPreferencesAction(Action):
    """An action that displays the preferences dialog."""

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = "Manage Preferences"

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource("preferences")

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Preferences"

    # A short description of the action used for tooltip text etc.
    tooltip = "Manage Preferences"

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """Performs the action."""

        from apptools.preferences.ui.api import PreferencesManager

        # Lookup the preferences manager service.
        manager = event.window.application.get_service(PreferencesManager)
        ui = manager.edit_traits(parent=event.window.control, kind="modal")

        # If the user hit the "Ok" button, then save the preferences in case
        # application crashes before it exits!
        if ui.result:
            self.window.application.preferences.save()
