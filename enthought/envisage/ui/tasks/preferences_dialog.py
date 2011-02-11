# Enthought library imports.
from enthought.traits.api import HasTraits, List, Property, cached_property

# Local imports.
from preferences_category import PreferencesCategory
from preferences_pane import PreferencesPane


class PreferencesDialog(HasTraits):
    """ A dialog for editing preferences.
    """

    #### 'PreferencesDialog' interface ########################################

    # The list of categories to use when building the dialog.
    categories = List(PreferencesCategory)

    # The list of panes to use when building the dialog.
    panes = List(PreferencesPane)

    #### Private interface ####################################################
    
    _categories = Property(List(PreferencesCategory), 
                           depends_on='categories, panes')
    _panes = Property(List(PreferencesPane), depends_on='_categories')

    ###########################################################################
    # Protected interface.
    ###########################################################################
    
    #### Private interface ####################################################

    @cached_property
    def _get__categories(self):
        categories = self.categories[:]
