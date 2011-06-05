""" The workbench preferences. """


# Enthought library imports.
from apptools.preferences.api import PreferencesHelper
from traits.api import Bool


class WorkbenchPreferences(PreferencesHelper):
    """ Helper for the workbench preferences. """

    #### 'PreferencesHelper' interface ########################################

    # The path to the preferences node that contains the preferences.
    preferences_path = 'envisage.ui.workbench'

    #### Preferences ##########################################################

    # Should the user be prompted before exiting the workbench?
    prompt_on_exit = Bool(True)

#### EOF ######################################################################
