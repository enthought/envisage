# (C) Copyright 2007-2025 Enthought, Inc., Austin, TX
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
    IPreferences,
    Preferences,
    PreferencesHelper,
    ScopedPreferences,
)
from traits.api import Instance, Str
from traitsui.api import Item, View

from envisage.ui.tasks.api import PreferencesPane


class MyPreferencesHelper(PreferencesHelper):
    #: Redeclare preferences to force trait copying order.
    preferences = Instance(IPreferences)

    #: The node that contains the preferences.
    preferences_path = Str("app")

    #: The user's favourite colour
    color = Str()


class MyPreferencesPane(PreferencesPane):
    model_factory = MyPreferencesHelper

    view = View(Item("color"))


class TestPreferencesPane(unittest.TestCase):
    def test_no_preference_changes_without_apply(self):
        # Regression test for https://github.com/enthought/envisage/issues/582

        # Given scoped preferences where the default preferences layer has
        # a value for app.color ...
        default_preferences = Preferences(name="default")
        application_preferences = Preferences(name="application")
        preferences = ScopedPreferences(
            scopes=[application_preferences, default_preferences]
        )
        default_preferences.set("app.color", "red")

        # When we create the preferences helper and pane, and trigger the
        # trait_context method (which will usually be called as part of
        # creating the TraitsUI UI).
        helper = MyPreferencesHelper(preferences=preferences)
        self.assertIsNone(application_preferences.get("app.color"))
        pane = MyPreferencesPane(model=helper)
        pane.trait_context()["object"]

        # Then the application preferences should not have been changed.
        self.assertIsNone(application_preferences.get("app.color"))
