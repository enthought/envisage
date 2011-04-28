""" Text Editor plugin definition. """


# Plugin extension-point imports.
from envisage import PluginDefinition, get_using_workbench


# Are we using the old UI plugin, or the shiny new Workbench plugin?
USING_WORKBENCH = get_using_workbench()

# Enthought plugin definition imports.
if USING_WORKBENCH:
    from envisage.workbench.action.action_plugin_definition import \
         Action, Group, Location, Menu, WorkbenchActionSet

else:
    from envisage.ui.ui_plugin_definition import \
         Action, Group, Menu, UIActions


# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "envisage.plugins.refresh_code"


###############################################################################
# Extensions.
###############################################################################

if USING_WORKBENCH:
    refresh_code = Action(
        name          = "Refresh Code",
        description   = "Refresh application to reflect python code changes",
        accelerator   = "Ctrl+Shift+R",
        function_name = "traits.util.refresh.refresh",

        locations     = [
            Location(path="MenuBar/FileMenu/ExitGroup")
        ]
    )

    actions = WorkbenchActionSet(
        id   = ID + ".refresh_code_action_set",
        name = "Refresh Code",

        # fixme: This menus stuff should go away once we get ticket:312
        # resolved.
        #groups = [
        #    Group(
        #        id = "ToolsMenuGroup",
        #        location = Location(path="MenuBar")
        #    ),
        #    Group(
        #        id = "RefreshGroup",
        #        location = Location(path="MenuBar/ToolsMenu")
        #    ),
        #],

        #menus = [
        #    Menu(
        #        id = "ToolMenu",
        #        name = "&Tools",
        #        location = Location(path="MenuBar/ToolsMenuGroup"),
        #        groups = []
        #    ),
        #],

        actions = [refresh_code]
    )

    requires = "envisage.workbench.action"

else:
    refresh_code = Action(
        name          = "Refresh Code", # fixme: this should change
        description   = "Refresh application to reflect python code changes",
        menu_bar_path = "ToolsMenu/additions", # fixme: this should change
        accelerator   = "Ctrl+Shift+R",
        function_name = "traits.util.refresh.refresh"
    )

    actions =  UIActions(
        # fixme: This menus stuff should go away once we get ticket:312
        # resolved.
        menus = [
            Menu(
                id     = "ToolsMenu",
                name   = "&Tools",
                path   = "ToolsGroup",

                groups = [
                    Group(id = "Start"),
                    Group(id = "End"),
                ]
            ),
        ],

        actions = [refresh_code]
    )

    requires = "envisage.ui"

###############################################################################
# The plugin definition!
###############################################################################

class RefreshCodePluginDefinition(PluginDefinition):
    # The plugin's globally unique identifier.
    id = ID

    # General information about the plugin.
    name          = "Refresh Code Plugin"
    version       = "1.0.0"
    provider_name = "Enthought Inc"
    provider_url  = "www.enthought.com"
    enabled       = True

    # The Id's of the plugins that this plugin requires.
    requires = [requires]

    # The extension points offered by this plugin,
    extension_points = []

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [actions]

#### EOF ######################################################################
