# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from apptools.preferences.api import PreferencesHelper
from traits.api import Bool, Dict, Str
from traitsui.api import EnumEditor, HGroup, Item, Label, VGroup, View

# Enthought library imports.
from envisage.ui.tasks.api import PreferencesPane


class AttractorsPreferences(PreferencesHelper):
    """The preferences helper for the Attractors application."""

    #### 'PreferencesHelper' interface ########################################

    # The path to the preference node that contains the preferences.
    preferences_path = "example.attractors"

    #### Preferences ##########################################################

    # The task to activate on app startup if not restoring an old layout.
    default_task = Str

    # Whether to always apply the default application-level layout.
    # See TasksApplication for more information.
    always_use_default_layout = Bool


class AttractorsPreferencesPane(PreferencesPane):
    """The preferences pane for the Attractors application."""

    #### 'PreferencesPane' interface ##########################################

    # The factory to use for creating the preferences model object.
    model_factory = AttractorsPreferences

    #### 'AttractorsPreferencesPane' interface ################################

    task_map = Dict(Str, Str)

    view = View(
        VGroup(
            HGroup(
                Item("always_use_default_layout"),
                Label("Always use the default active task on startup"),
                show_labels=False,
            ),
            HGroup(
                Label("Default active task:"),
                Item(
                    "default_task", editor=EnumEditor(name="handler.task_map")
                ),
                enabled_when="always_use_default_layout",
                show_labels=False,
            ),
            label="Application startup",
        ),
        resizable=True,
    )

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _task_map_default(self):
        return dict(
            (factory.id, factory.name)
            for factory in self.dialog.application.task_factories
        )
