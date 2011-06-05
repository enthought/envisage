#-----------------------------------------------------------------------------
#
#  Copyright (c) 2006 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

""" Preference page for default path for a project
"""

# Enthought library imports
from apptools.preferences.ui.api import PreferencesPage
from traits.api import Directory, Str
from traitsui.api import View, Item

# Global assignment of ID
ID = 'envisage.ui.single_project'

#-------------------------------------------------------------------------------
#   DefaultPathPreferencePage Class
#-------------------------------------------------------------------------------

class DefaultPathPreferencePage(PreferencesPage):
    """ Preference page for default path for a plugin.
    """

    # The page name (this is what is shown in the preferences dialog.
    name = 'Single Project'

    # The path to the preferences node that contains the preferences.
    preferences_path = 'envisage.ui.single_project'

    #### Preferences ##########################################################

    # Choose the unit system that needs to be used for the project
    preferred_path = Directory('')

    # Set the traits view
    traits_view = View(Item('preferred_path', style='custom',
        tooltip='Path that will be used for storing projects'))

### EOF ------------------------------------------------------------------------
