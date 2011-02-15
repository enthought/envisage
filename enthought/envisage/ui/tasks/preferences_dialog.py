# Enthought library imports.
from enthought.traits.api import Bool, HasTraits, List, Property, Unicode, \
    cached_property
from enthought.traits.ui.api import Item, ListEditor, View 
from enthought.pyface.tasks.topological_sort import before_after_sort

# Local imports.
from preferences_category import PreferencesCategory
from preferences_pane import PreferencesPane


class PreferencesTab(HasTraits):
    """ An object used internally by PreferencesDialog.
    """
    
    name = Unicode
    panes = List(PreferencesPane)

    view = View(Item('panes',
                     editor = ListEditor(style = 'custom'),
                     show_label = False,
                     style = 'readonly'),
                resizable = True)


class PreferencesDialog(HasTraits):
    """ A dialog for editing preferences.
    """

    #### 'PreferencesDialog' interface ########################################

    # The list of categories to use when building the dialog.
    categories = List(PreferencesCategory)

    # The list of panes to use when building the dialog.
    panes = List(PreferencesPane)

    # Should the Apply button be shown?
    show_apply = Bool(False)

    #### Private interface ####################################################
    
    _tabs = Property(List(PreferencesTab), depends_on='categories, panes')

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################
    
    def traits_view(self):
        """ Build the dynamic dialog view.
        """
        buttons = ['OK', 'Cancel']
        if self.show_apply:
            buttons = ['Apply'] + buttons

        # Only show the tab bar if there is more than one category.
        tabs_style = 'custom' if len(self._tabs) > 1 else 'readonly'

        return View(Item('_tabs',
                         editor = ListEditor(page_name = '.name', 
                                             style ='custom',
                                             use_notebook = True),
                         show_label = False,
                         style = tabs_style),
                    buttons = buttons,
                    kind = 'modal',
                    resizable = True,
                    title = 'Preferences')

    ###########################################################################
    # Protected interface.
    ###########################################################################
    
    @cached_property
    def _get__tabs(self):
        # Build a { category id -> [ PreferencePane ] } map.
        categories = self.categories[:]
        category_map = dict((category.id, []) for category in categories)
        for pane in self.panes:
            if pane.category in category_map:
                category_map[pane.category].append(pane)
            else:
                categories.append(PreferencesCategory(id=pane.category))
                category_map[pane.category] = [ pane ]

        # Construct the appropriately sorted list of preference tabs.
        return [ PreferencesTab(name = cat.name,
                                panes = before_after_sort(category_map[cat.id]))
                 for cat in before_after_sort(categories) ]
