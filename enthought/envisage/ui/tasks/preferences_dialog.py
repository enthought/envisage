# Enthought library imports.
from enthought.traits.api import Bool, HasTraits, List, Unicode, on_trait_change
from enthought.traits.ui.api import Item, Handler, ListEditor, View
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


class PreferencesDialog(Handler):
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
    
    _tabs = List(PreferencesTab)

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################

    def trait_context ( self ):
        """ Returns the default context to use for editing or configuring
            traits.
        """
        return { 'object': self, 'handler': self }
    
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
                    kind = 'livemodal',
                    resizable = True,
                    title = 'Preferences')

    ###########################################################################
    # 'Handler' interface.
    ###########################################################################

    def apply(self, info=None):
        """ Handles the Apply button being clicked.
        """
        for tab in self._tabs:
            for pane in tab.panes:
                pane.apply()

    def close(self, info, is_ok):
        """ Handles the user attempting to close a dialog-based user interface.
        """
        if is_ok:
            self.apply()
        return super(PreferencesDialog, self).close(info, is_ok)

    ###########################################################################
    # Protected interface.
    ###########################################################################
    
    @on_trait_change('categories, panes')
    def _update_tabs(self):
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
        tabs = []
        for category in before_after_sort(categories):
            panes = before_after_sort(category_map[category.id])
            tabs.append(PreferencesTab(name = category.name, panes=panes))
        self._tabs = tabs
