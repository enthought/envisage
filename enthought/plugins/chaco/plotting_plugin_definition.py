""" The plotting plugin definition. """


# Enthought library imports.
from enthought.traits.api import List, Str

# Plugin definition imports.
from enthought.envisage.core.core_plugin_definition \
     import ExtensionItem, ExtensionPoint, PluginDefinition

from enthought.envisage.ui.ui_plugin_definition \
     import Action, EnabledWhen, Group, Menu, UIActions

from enthought.envisage.resource.resource_ui_plugin_definition \
     import CookieImplementation, CookieImplementations, \
     ResourceAction, ResourceActions, ResourceMenu


# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "enthought.plugins.chaco"

###############################################################################
# Extension Points.
###############################################################################

class PlotDataFactory(ExtensionItem):
    """ A plot data factory for a resource type or types. """

    # The class name of the plot data factory.
    class_name = Str

    # The resource types that the factory handles.
    resource_types = List(Str)

class PlotDataFactories(ExtensionPoint):
    """ Allows other plugins to contribute a plot data factory. """

    # PlotDataFactory contributions.
    factories = List(PlotDataFactory)

class PlotTemplateFactory(ExtensionItem):
    """ A facotry for producing a plot template for a resource type. """

    # The class name which implements the factory.
    class_name = Str

    # The category to display the template.
    category = Str

    # The name of the factory.
    name = Str

    # The resource types that the factory handles.
    resource_types = List(Str)

class PlotTemplateFactories(ExtensionPoint):
    """ Allows other plugins to contribute a plot template factory. """

    # PlotTemplateFactory contributions.
    factories = List(PlotTemplateFactory)


###############################################################################
# Extensions.
###############################################################################

ui_actions = UIActions(
    actions = [
        Action(
            id            = ID + ".action.plot_cookie_action.PlotCookieAction",
            class_name    = ID + ".action.plot_cookie_action.PlotCookieAction",
            name          = "Plot",
            description   = "Plot the selected resource",
            tooltip       = "Plot the selected resource",

            tool_bar_path = "additions",
            enabled = False,
            enabled_when  = EnabledWhen(
                cookie = ID + ".cookie.plot_cookie.PlotCookie"
            )
        )
    ]
)

#### Resource Actions #########################################################

resource_actions = ResourceActions(

    actions = [
        ResourceAction(
            id            = ID + ".action.plot_cookie_action.PlotCookieAction",
            class_name    = ID + ".action.plot_cookie_action.PlotCookieAction",
            name          = "Plot",
            description   = "Plot the selected resource",
            tooltip       = "Plot the selected resource",

            resource_type = "",
            path          = "system_top",

            enabled_when  = EnabledWhen(
                cookie = ID + ".cookie.plot_cookie.PlotCookie"
            )

        ),

        ResourceAction(
            id            = ID + ".action.plot_as_cookie_action.PlotAsCookieAction",
            class_name    = ID + ".action.plot_as_cookie_action.PlotAsCookieAction",
            name          = "Plot As...",
            description   = "Plot the selected resource with a template",
            tooltip       = "Plot the selected resource with a template",

            resource_type = "",
            path          = "system_top",

            enabled_when  = EnabledWhen(
                cookie = ID + ".cookie.plot_as_cookie.PlotAsCookie"
            )
        )
    ],
)

#### The plugin defintion! ####################################################

PluginDefinition(
    # The plugin's globally unique identifier.
    id = ID,

    # The name of the class that implements the plugin.
    class_name = ID + ".plotting_plugin.PlottingPlugin",

    # General information about the plugin.
    name          = "Chaco Plotting Plugin",
    version       = "0.0.1",
    provider_name = "Enthought Inc",
    provider_url  = "www.enthought.com",
    enabled       = True,
    autostart     = True,

    # The Id's of the plugins that this plugin requires.
    requires = ["enthought.envisage.ui", "enthought.envisage.resource",
                "enthought.envisage.resource_ui",
                ],

    # The extension points offered by this plugin.
    extension_points = [PlotDataFactories],

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [resource_actions], # ui_actions
)


#### EOF ######################################################################
