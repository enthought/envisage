# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# Enthought library imports.
from apptools.preferences.api import IPreferences, PreferencesHelper
from traits.api import Callable, Dict, HasTraits, Instance, Str
from traitsui.api import Controller


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

    # The preferences dialog to which the pane belongs. Set by the framework.
    dialog = Instance(
        'envisage.ui.tasks.preferences_dialog.PreferencesDialog')

    # # The factory to use for creating the preferences model object, of form:
    #     callable(**traits) -> PreferencesHelper
    # If not specified, the preferences helper must be supplied manually.
    model_factory = Callable

    #### Private interface ####################################################

    _model = Instance(PreferencesHelper)

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################

    def trait_context ( self ):
        """ Re-implemented to use a copy of the model that is not connected to
            the preferences node.
        """
        if self.model is None:
            if self.model_factory is not None:
                preferences = self.dialog.application.preferences
                self.model = self.model_factory(preferences = preferences)
            else:
                raise ValueError('A preferences pane must have a model!')

        self._model = self.model.clone_traits()
        self._model.preferences = None
        return { 'object': self._model, 'controller': self, 'handler': self }

    ###########################################################################
    # 'Handler' interface.
    ###########################################################################

    def apply(self, info=None):
        """ Handles the Apply button being clicked.
        """
        trait_names = list(filter(self._model._is_preference_trait,
                                  self._model.trait_names()))
        self.model.copy_traits(self._model, trait_names)

    def close(self, info, is_ok):
        """ Handles the user attempting to close a dialog-based user interface.
        """
        if is_ok:
            self.apply()
        return super(PreferencesPane, self).close(info, is_ok)
