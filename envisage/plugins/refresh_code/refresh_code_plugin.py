# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A plugin that offers the 'refresh code' functionality. """


# Enthought library imports.
from envisage.api import Plugin
from traits.api import List


class RefreshCodePlugin(Plugin):
    """ A plugin that offers the 'refresh code' functionality. """

    # Extension point Ids.
    ACTION_SETS = 'envisage.ui.workbench.action_sets'

    #### Extension points offered by this plugin ##############################

    # None.

    #### Contributions to extension points made by this plugin ################

    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """

        from envisage.plugins.refresh_code.refresh_code_action_set import (
            RefreshCodeActionSet
        )

        return [RefreshCodeActionSet]

#### EOF ######################################################################
