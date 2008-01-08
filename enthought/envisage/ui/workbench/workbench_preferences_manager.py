""" The preferences manager for the workbench. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint
from enthought.preferences.ui.api import PreferencesManager, IPreferencesPage
from enthought.traits.api import List


class WorkbenchPreferencesManager(PreferencesManager):
    """ The preferences manager for the workbench. """

    # Extension point Ids.
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'
    
    #### Private interface ####################################################

    # All of the preferences pages known to the manager.
    #
    # fixme: We have this as a shadowed private trait so that we only get
    # the pages from the extension registry *once* - otherwise every time we
    # access the trait we get new pages!!!! This is a fundemental issue with
    # the way we do extension at the moment.... hmmmm....
    _pages = ExtensionPoint(List(IPreferencesPage), id=PREFERENCES_PAGES)

    ###########################################################################
    # 'PreferencesManager' interface.
    ###########################################################################

    def _pages_default(self):
        """ Trait initializer. """

        # We use an initializer like this to make sure we only get the
        # contributed pages *once*. Otherwise, every time we access the trait
        # we get new ones!
        return self._pages
    
#### EOF ######################################################################
