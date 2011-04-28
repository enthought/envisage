#-------------------------------------------------------------------------------
#
#  FBI (Frame Based Inspector) Plugin.
#
#  Written by: David C. Morrill
#
#  Date: 1/4/2006
#
#  (c) Copyright 2006 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from envisage.core.core_plugin_definition \
    import PluginDefinition

#-------------------------------------------------------------------------------
# The plugin definition:
#-------------------------------------------------------------------------------

PluginDefinition(
    # The plugin's globally unique identifier:
    id = "envisage.plugins.debug.fbi",

    # The name of the class that implements the plugin:
    class_name = "envisage.plugins.debug.fbi_plugin.FBIPlugin",

    # General information about the plugin:
    name          = "FBI Plugin",
    version       = "1.0.0",
    provider_name = "Enthought Inc",
    provider_url  = "www.enthought.com",
    enabled       = True,
    autostart     = True,

    # The Id's of the plugins that this plugin requires:
    requires = [
        "envisage.core",
    ]
)

