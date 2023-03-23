# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# Enthought library imports.
from pyface.tasks.topological_sort import before_after_sort
from traits.api import Bool, HasTraits, Instance, List, on_trait_change, Str
from traitsui.api import Handler, Item, ListEditor, View

# Local imports.
from .preferences_category import PreferencesCategory
from .preferences_pane import PreferencesPane


class PreferencesTab(HasTraits):
    """An object used internally by PreferencesDialog."""

    name = Str
    panes = List(PreferencesPane)

    view = View(
        Item(
            "panes",
            editor=ListEditor(style="custom"),
            show_label=False,
            style="readonly",
        ),
        resizable=True,
    )


class PreferencesDialog(Handler):
    """A dialog for editing preferences."""

    #### 'PreferencesDialog' interface ########################################

    # The application that created and is managing this dialog.
    application = Instance("envisage.ui.tasks.api.TasksApplication")

    # The list of categories to use when building the dialog.
    categories = List(PreferencesCategory)

    # The list of panes to use when building the dialog.
    panes = List(PreferencesPane)

    # Should the Apply button be shown?
    show_apply = Bool(False)

    #### Private interface ####################################################

    _tabs = List(PreferencesTab)
    _selected = Instance(PreferencesTab)

    ###########################################################################
    # Public interface
    ###########################################################################

    def select_pane(self, pane_id):
        """
        Find and activate the notebook tab that contains the given pane id.
        """
        for tab in self._tabs:
            for pane in tab.panes:
                if pane.id == pane_id:
                    self._selected = tab
                    return

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################

    def trait_context(self):
        """Returns the default context to use for editing or configuring
        traits.
        """
        return {"object": self, "handler": self}

    def traits_view(self):
        """Build the dynamic dialog view."""
        buttons = ["OK", "Cancel"]
        if self.show_apply:
            buttons = ["Apply"] + buttons

        # Only show the tab bar if there is more than one category.
        tabs_style = "custom" if len(self._tabs) > 1 else "readonly"

        return View(
            Item(
                "_tabs",
                editor=ListEditor(
                    page_name=".name",
                    style="custom",
                    use_notebook=True,
                    selected="_selected",
                ),
                show_label=False,
                style=tabs_style,
            ),
            buttons=buttons,
            kind="livemodal",
            resizable=True,
            title="Preferences",
        )

    ###########################################################################
    # 'Handler' interface.
    ###########################################################################

    def apply(self, info=None):
        """Handles the Apply button being clicked."""
        for tab in self._tabs:
            for pane in tab.panes:
                pane.apply()

    def close(self, info, is_ok):
        """
        Handles the user attempting to close a dialog-based user interface.
        """
        if is_ok:
            self.apply()
        return super().close(info, is_ok)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @on_trait_change("categories, panes")
    def _update_tabs(self):
        # Build a { category id -> [ PreferencePane ] } map.
        categories = self.categories[:]
        category_map = dict((category.id, []) for category in categories)
        for pane in self.panes:
            if pane.category in category_map:
                category_map[pane.category].append(pane)
            else:
                categories.append(PreferencesCategory(id=pane.category))
                category_map[pane.category] = [pane]

        # Construct the appropriately sorted list of preference tabs.
        tabs = []
        for category in before_after_sort(categories):
            panes = before_after_sort(category_map[category.id])
            tabs.append(PreferencesTab(name=category.name, panes=panes))
        self._tabs = tabs
