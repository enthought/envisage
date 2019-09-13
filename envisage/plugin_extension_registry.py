# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An extension registry that uses plugins as extension providers. """


# Enthought library imports.
from traits.api import Instance, on_trait_change

# Local imports.
from .i_plugin_manager import IPluginManager
from .provider_extension_registry import ProviderExtensionRegistry


class PluginExtensionRegistry(ProviderExtensionRegistry):
    """ An extension registry that uses plugins as extension providers.

    The application's plugins are used as the registries providers so adding
    or removing a plugin affects the extension points and extensions etc.

    """

    #### 'PluginExtensionRegistry' interface ##################################

    # The plugin manager that has the plugins we are after!
    plugin_manager = Instance(IPluginManager)

    ###########################################################################
    # 'PluginExtensionRegistry' interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _plugin_manager_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        # In practise I can't see why you would ever want (or need) to change
        # the registry's plugin manager on the fly, but hey... Hence, 'old'
        # will probably always be 'None'!
        if old is not None:
            for plugin in old:
                self.remove_provider(plugin)

        if new is not None:
            for plugin in new:
                self.add_provider(plugin)

        return

    @on_trait_change('plugin_manager:plugin_added')
    def _on_plugin_added(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        self.add_provider(event.plugin)

        return

    @on_trait_change('plugin_manager:plugin_removed')
    def _on_plugin_removed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        self.remove_provider(event.plugin)

        return

#### EOF ######################################################################
