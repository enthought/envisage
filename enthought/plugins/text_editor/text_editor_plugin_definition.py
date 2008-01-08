""" Text Editor plugin definition. """


# Enthought library imports.
from enthought.envisage import PluginDefinition

# Plugin definition imports.
from enthought.envisage.workbench.action.action_plugin_definition import \
     Action, Group, Location, Menu, WorkbenchActionSet


# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "enthought.plugins.text_editor"


###############################################################################
# Extensions.
###############################################################################

# Service Ids used in actions.
IWORKBENCH_UI = "enthought.envisage.workbench.IWorkbenchUI"


text_file_action_set = WorkbenchActionSet(
    id   = ID + ".text_file_action_set",
    name = "TextFile",

    groups = [
        Group(
            id = "TextFileGroup",
            location = Location(path="MenuBar/FileMenu", before="ExitGroup")
        )
    ],

    actions = [
        Action(
            id = "NewFileAction",
            name = "New File",
            tooltip = "Create a new file for editing",
            description = "Create a new file for editing",

            object = "service://" + IWORKBENCH_UI,
            method_name = "new_file",

            locations = [
                Location(path="MenuBar/FileMenu/TextFileGroup")
            ]
        ),

        Action(
            id = 'OpenFile',
            name = "Open File...",
            tooltip = "Open a file for editing",
            description = "Open a file for editing",

            object = "service://" + IWORKBENCH_UI,
            method_name = "open_file",

            locations = [
                Location(path="MenuBar/FileMenu/TextFileGroup")
            ]
        )
    ]
)

###############################################################################
# The plugin definition!
###############################################################################

class TextEditorPluginDefinition(PluginDefinition):
    """ The text editor plugin. """

    # The plugin's globally unique identifier.
    id = ID

    # General information about the plugin.
    name          = "Text Editor Plugin"
    version       = "1.0.0"
    provider_name = "Enthought Inc"
    provider_url  = "www.enthought.com"

    # The Id's of the plugins that this plugin requires.
    requires = ["enthought.envisage.workbench.action"]

    # The extension points offered by this plugin,
    extension_points = []

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [text_file_action_set]

#### EOF ######################################################################
