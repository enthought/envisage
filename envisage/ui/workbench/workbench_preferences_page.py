# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The main preferences page for the workbench. """


# Enthought library imports.
from apptools.preferences.ui.api import PreferencesPage
from traits.api import Bool
from traitsui.api import View


class WorkbenchPreferencesPage(PreferencesPage):
    """ The main preferences page for the workbench. """

    #### 'PreferencesPage' interface ##########################################

    # The page's category (e.g. 'General/Appearance'). The empty string means
    # that this is a top-level page.
    category = ''

    # The page's help identifier (optional). If a help Id *is* provided then
    # there will be a 'Help' button shown on the preference page.
    help_id = ''

    # The page name (this is what is shown in the preferences dialog.
    name = 'General'

    # The path to the preferences node that contains the preferences.
    preferences_path = 'envisage.ui.workbench'

    #### Preferences ##########################################################

    # Should the user be prompted before exiting the workbench?
    prompt_on_exit = Bool(True)

    #### Traits UI views ######################################################

    trait_view = View('prompt_on_exit')

#### EOF ######################################################################
