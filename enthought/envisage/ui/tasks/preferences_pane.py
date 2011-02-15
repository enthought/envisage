# Enthought library imports.
from enthought.traits.api import HasTraits, Str
from enthought.traits.ui.api import Controller


class PreferencesPane(Controller):
    """ A panel for configuring application preferences.
    
    Usually the 'model' attribute should be a PreferencesHelper.
    """

    # An identifier for the pane (unique within a category).
    id = Str

    # The ID of the category in which to place the pane.
    category = Str('General')

    # The pane appears after the pane with this ID.
    before = Str

    # The pane appears after the pane with this ID.
    after = Str
