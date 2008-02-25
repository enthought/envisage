""" The preferences manager for the workbench. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint
from enthought.preferences.ui.api import PreferencesManager, IPreferencesPage


class WorkbenchPreferencesManager(PreferencesManager):
    """ The preferences manager for the workbench. """

    # Extension point Ids.
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'
    
    #### Private interface ####################################################

    # Contributed preferences page factories.
    _page_factories = ExtensionPoint(id=PREFERENCES_PAGES)

    ###########################################################################
    # 'PreferencesManager' interface.
    ###########################################################################

    def _pages_default(self):
        """ Trait initializer. """

        pages = []
        for factory_or_page in self._page_factories:
            # Is the contribution an actual preferences page, or is it a
            # factory that can create a preferences page?
            page = IPreferencesPage(factory_or_page, None)
            if page is None:
                page = factory_or_page()

            pages.append(page)
                
        return pages
    
#### EOF ######################################################################
