""" The plotting plugin definition. """


# Enthought library imports.
from enthought.traits.api import List, Str

# Plugin definition imports.
from enthought.envisage.core.core_plugin_definition import PluginDefinition

from enthought.envisage.ui.python_shell.python_shell_plugin_definition \
     import Namespace

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "enthought.plugins.chaco.plt"


###############################################################################
# Extensions.
###############################################################################

namespace = Namespace(
    commands = [
        'from enthought.plugins.chaco.plt import *',
        'from enthought.chaco.default_colormaps import *'
    ]
)

#### The plugin defintion! ####################################################

PluginDefinition(
    # The plugin's globally unique identifier.
    id = ID,

    # The name of the class that implements the plugin.
    class_name = "enthought.plugins.chaco.plt_plugin.PltPlugin",

    # General information about the plugin.
    name          = "Chaco Interactive Plotting Plugin",
    version       = "0.0.1",
    provider_name = "Enthought Inc",
    provider_url  = "www.enthought.com",
    enabled       = True,
    autostart     = True,

    # The Id's of the plugins that this plugin requires.
    requires = ["enthought.envisage.ui.python_shell"],

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [namespace],
)


#### EOF ######################################################################
