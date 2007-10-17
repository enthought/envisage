""" An extension registry that uses plugins as extension providers. """


# Enthought library imports.
from enthought.traits.api import Instance, List, on_trait_change

# Local imports.
from i_application import IApplication
from i_extension_provider import IExtensionProvider
from provider_extension_registry import ProviderExtensionRegistry


class PluginExtensionRegistry(ProviderExtensionRegistry):
    """ An extension registry that uses plugins as extension providers. """

    #### 'IProviderExtensionRegistry' interface ###############################

    # The extension providers that populate the registry.
    #
    # There is currently no way to express this in traits, but this trait is
    # readonly, meaning that you can use the list to iterate over all of the
    # items in it, and you can listen for changes to the list, but if you want
    # to add or remove a provider you should call 'add_provider' or
    # 'remove_provider' respectively.
    providers = List(IExtensionProvider)

    #### 'PluginExtensionRegistry' interface ##################################

    # The application that the registry is part of.
    application = Instance(IApplication)

    ###########################################################################
    # 'PluginExtensionRegistry' interface.
    ###########################################################################

    @on_trait_change('application.plugin_added')
    def _on_plugin_added(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        if trait_name == 'plugin_added':
            self.add_provider(event.plugin)

        return

    @on_trait_change('application.plugin_removed')
    def _on_plugin_removed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        if trait_name == 'plugin_removed':
            self.remove_provider(event.plugin)

        return
    
    #### Trait change handlers ################################################

    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        if old is not None:
            for plugin in old.get_plugins():
                self.remove_provider(plugin)

        if new is not None:
            for plugin in new.get_plugins():
                self.add_provider(plugin)

        return

#### EOF ######################################################################
