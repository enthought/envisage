# (C) Copyright 2007-2024 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The preferences for the Acme workbench. """


# Enthought library imports.
from apptools.preferences.ui.api import PreferencesPage
from traits.api import Float, Int
from traitsui.api import Color, Font, View


class AcmePreferencesPage(PreferencesPage):
    """The preferences page for the Acme workbench."""

    #### 'PreferencesPage' interface ##########################################

    # The page's category (e.g. 'General/Appearance'). The empty string means
    # that this is a top-level page.
    category = "General"

    # The page's help identifier (optional). If a help Id *is* provided then
    # there will be a 'Help' button shown on the preference page.
    help_id = ""

    # The page name (this is what is shown in the preferences dialog.
    name = "Acme"

    # The path to the preference node that contains the preferences.
    preferences_path = "acme.workbench"

    #### Preferences ##########################################################

    # Width.
    width = Int(100)

    # Height.
    height = Int(200)

    # Ratio.
    ratio = Float(0.1)

    # Background color.
    bgcolor = Color("red")

    # Text font.
    font = Font("helvetica")

    #### Traits UI views ######################################################

    trait_view = View("width", "height", "ratio", "font", "bgcolor")
