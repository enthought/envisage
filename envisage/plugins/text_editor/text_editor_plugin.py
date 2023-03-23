# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Text Editor plugin for the Workbench UI.
"""


# Enthought library imports.
from traits.api import List

from envisage.api import Plugin

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "envisage.plugins.text_editor"


class TextEditorPlugin(Plugin):
    """Text Editor plugin for the Workbench UI."""

    name = "Text Editor plugin"

    #### Contributions made by this plugin ####################################

    ACTION_SETS = "envisage.ui.workbench.action_sets"
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        from envisage.plugins.text_editor.text_editor_action_set import (
            TextEditorActionSet,
        )

        return [TextEditorActionSet]
