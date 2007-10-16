""" An extension registry that uses plugins as extension providers. """


# Enthought library imports.
from enthought.traits.api import Instance, on_trait_change

# Local imports.
from i_application import IApplication
from provider_extension_registry import ProviderExtensionRegistry


class PluginExtensionRegistry(ProviderExtensionRegistry):
    """ An extension registry that uses plugins as extension providers. """
    
    #### 'PluginProviderExtensionRegistry' interface ##########################

    # The application that the registry is part of.
    application = Instance(IApplication)

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    @on_trait_change(
        'application.plugin_manager.plugins,'
        'application.plugin_manager.plugins_items'
    )
    def _plugins_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        if trait_name == 'plugins':
            added   = new
            removed = old

        elif trait_name == 'plugins_items':
            added   = new.added
            removed = new.removed

        elif trait_name == 'plugin_manager':
            added   = new is not None and new.plugins or []
            removed = old is not None and old.plugins or []

        else:
            assert trait_name=='application'
                
            if new is not None and new.plugin_manager is not None:
                added = new.plugin_manager.plugins

            else:
                added = []

            if old is not None and old.plugin_manager is not None:
                removed = old.plugin_manager.plugins

            else:
                removed = []

        self._update_providers(added, removed)

        return

    #### Methods ##############################################################

    def _update_providers(self, added, removed):
        """ Add/remove the specified providers. """

        for plugin in removed:
            self.remove_provider(plugin)

        for plugin in added:
            self.add_provider(plugin)

        return

#### EOF ######################################################################
