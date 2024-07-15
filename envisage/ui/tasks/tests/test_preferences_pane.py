# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""Tests for the PreferencesPane."""


import unittest


from apptools.preferences.api import (
    Preferences,
    PreferencesHelper,
    ScopedPreferences,
)
from traits.api import Str
from traitsui.api import Item, View

from envisage.ui.tasks.api import PreferencesPane


class MyPreferences(PreferencesHelper):
    #: The node that contains the preferences.
    preferences_path = "app"

    #: The user's favourite colour
    color = Str()


class MyPreferencesPane(PreferencesPane):

    model_factory = MyPreferences

    view = View(
        Item("color"),
    )


class TestPreferencesPane(unittest.TestCase):
    def test_no_preference_changes_without_apply(self):
        # Regression test for https://github.com/enthought/envisage/issues/582
        default_preferences = Preferences(name="default")
        default_preferences.set("app.color", "red")

        application_preferences = Preferences(name="application")
        preferences = ScopedPreferences(
            scopes=[application_preferences, default_preferences]
        )

        helper = MyPreferences(preferences=preferences)
        self.assertIsNone(application_preferences.get("app.color"))
        pane = MyPreferencesPane(model=helper)

        object_context = pane.trait_context()["object"]

        # At this point, the application preferences should still not
        # have an app.color setting
        self.assertIsNone(object_context.color)
