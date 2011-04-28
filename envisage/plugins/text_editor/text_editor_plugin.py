""" Text Editor plugin for the Workbench UI.
"""


# Enthought library imports.
from traits.api import List
from envisage.api import Plugin


# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "envisage.plugins.text_editor"


class TextEditorPlugin(Plugin):
    """ Text Editor plugin for the Workbench UI.
    """

    name = 'Text Editor plugin'

    #### Contributions made by this plugin #####################################

    ACTION_SETS = 'envisage.ui.workbench.action_sets'
    action_sets = List(contributes_to=ACTION_SETS)


    def _action_sets_default(self):
        from envisage.plugins.text_editor.text_editor_action_set import \
            TextEditorActionSet
        return [TextEditorActionSet]
