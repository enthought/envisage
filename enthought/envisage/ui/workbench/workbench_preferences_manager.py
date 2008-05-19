""" The preferences manager for the workbench. """


# Enthought library imports.
from enthought.preferences.ui.api import PreferencesManager, IPreferencesPage
from enthought.traits.api import Callable, List


class WorkbenchPreferencesManager(PreferencesManager):
    """ The preferences manager for the workbench. """

    # Extension point Ids.
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'

    #### Private interface ####################################################

    # Factories for the actual preferences pages.
    page_factories = List(Callable)

    ###########################################################################
    # 'PreferencesManager' interface.
    ###########################################################################

    def _pages_default(self):
        """ Trait initializer. """
        
        pages = []
        for factory_or_page in self.page_factories:
            # Is the contribution an actual preferences page, or is it a
            # factory that can create a preferences page?
            page = IPreferencesPage(factory_or_page, None)
            if page is None:
                page = factory_or_page()

            else:
                logger.warn(
                    'DEPRECATED: contribute preferences page classes or '
                    'factories - not preferences page instances.'
                )
                
            pages.append(page)
                
        return pages
    
#### EOF ######################################################################
