# Enthought library imports.
from enthought.preferences.api import IPreferences, PreferencesHelper
from enthought.traits.api import Dict, HasTraits, Instance, Str
from enthought.traits.ui.api import Controller


class PreferencesPane(Controller):
    """ A panel for configuring application preferences.
    """

    #### 'Controller' interface ###############################################

    # The preferences helper for which this pane is a view.
    model = Instance(PreferencesHelper)

    #### 'PreferencesPane' interface ##########################################

    # An identifier for the pane (unique within a category).
    id = Str

    # The ID of the category in which to place the pane.
    category = Str('General')

    # The pane appears after the pane with this ID.
    before = Str

    # The pane appears after the pane with this ID.
    after = Str

    #### Private interface ####################################################

    _model = Instance(PreferencesHelper)

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################

    def trait_context ( self ):
        """ Re-implemented to use a copy of the model that is not connected to
            the preferences node.
        """
        self._model = self.model.clone_traits()
        self._model.preferences = None
        return { 'object': self._model, 'controller': self, 'handler': self }

    ###########################################################################
    # 'Handler' interface.
    ###########################################################################

    def apply(self, info=None):
        """ Handles the Apply button being clicked.
        """
        trait_names = filter(self._model._is_preference_trait, 
                             self._model.trait_names())
        self.model.copy_traits(self._model, trait_names)

    def close(self, info, is_ok):
        """ Handles the user attempting to close a dialog-based user interface.
        """
        if is_ok:
            self.apply()
        return super(PreferencesPane, self).close(info, is_ok)
