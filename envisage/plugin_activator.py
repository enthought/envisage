# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The default plugin activator. """


# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_plugin_activator import IPluginActivator


@provides(IPluginActivator)
class PluginActivator(HasTraits):
    """ The default plugin activator. """

    ###########################################################################
    # 'IPluginActivator' interface.
    ###########################################################################

    def start_plugin(self, plugin):
        """ Start the specified plugin. """

        # Connect all of the plugin's extension point traits so that the plugin
        # will be notified if and when contributions are added or removed.
        plugin.connect_extension_point_traits()

        # Register all services.
        plugin.register_services()

        # Plugin specific start.
        plugin.start()

        return

    def stop_plugin(self, plugin):
        """ Stop the specified plugin. """

        # Plugin specific stop.
        plugin.stop()

        # Unregister all service.
        plugin.unregister_services()

        # Disconnect all of the plugin's extension point traits.
        plugin.disconnect_extension_point_traits()

        return

#### EOF ######################################################################
