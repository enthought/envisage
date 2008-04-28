""" A plugin that offers the 'refresh code' functionality. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class RefreshCodePlugin(Plugin):
    """ A plugin that offers the 'refresh code' functionality. """

    # Extension point Ids.
    ACTION_SETS = 'enthought.envisage.ui.workbench.action_sets'
    
    #### Extension points offered by this plugin ##############################

    # None.

    #### Contributions to extension points made by this plugin ################

    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """

        from enthought.plugins.refresh_code.refresh_code_action_set import (
            RefreshCodeActionSet
        )
        
        return [RefreshCodeActionSet]

#### EOF ######################################################################
