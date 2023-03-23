# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The workbench preferences. """


# Enthought library imports.
from apptools.preferences.api import PreferencesHelper
from traits.api import Bool


class WorkbenchPreferences(PreferencesHelper):
    """Helper for the workbench preferences."""

    #### 'PreferencesHelper' interface ########################################

    # The path to the preferences node that contains the preferences.
    preferences_path = "envisage.ui.workbench"

    #### Preferences ##########################################################

    # Should the user be prompted before exiting the workbench?
    prompt_on_exit = Bool(True)
