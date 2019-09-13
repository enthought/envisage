# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# Enthought library imports.
from pyface.action.api import Action, Group


class PreferencesAction(Action):
    """ An action that displays the preferences dialog.
    """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Open the preferences dialog'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Prefere&nces...'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Open the preferences dialog'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        from envisage.ui.tasks.preferences_dialog import \
            PreferencesDialog

        window = event.task.window
        dialog = window.application.get_service(PreferencesDialog)
        ui = dialog.edit_traits(parent=window.control, kind='livemodal')

        if ui.result:
            window.application.preferences.save()


class PreferencesGroup(Group):
    """ A group that contains the preferences action.
    """

    #### 'Action' interface ###################################################

    # The group's identifier (unique within action manager).
    id = 'PreferencesGroup'

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        super(PreferencesGroup, self).__init__(PreferencesAction(), **traits)
