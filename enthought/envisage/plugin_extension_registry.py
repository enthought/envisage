""" An extension registry that uses plugins as extension providers. """


# Enthought library imports.
from enthought.traits.api import Instance, on_trait_change

# Local imports.
from i_application import IApplication
from provider_extension_registry import ProviderExtensionRegistry


class PluginExtensionRegistry(ProviderExtensionRegistry):
    """ An extension registry that uses plugins as extension providers. """

    #### 'PluginExtensionRegistry' interface ##################################

    # The application that the registry is part of.
    application = Instance(IApplication)

    ###########################################################################
    # 'PluginExtensionRegistry' interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        # In practise I can't see why you would ever want (or need) to change
        # the registry's application on the fly, but hey... Hence, 'old' will
        # probably always be 'None'!
        if old is not None:
            for plugin in old:
                self.remove_provider(plugin)
                
        if new is not None:
            for plugin in new:
                self.add_provider(plugin)

        return

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

#### EOF ######################################################################
