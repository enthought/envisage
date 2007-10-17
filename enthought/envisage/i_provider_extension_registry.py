""" The provider extension registry interface. """


# Enthought library imports.
from enthought.traits.api import Event

# Local imports.
from i_extension_registry import IExtensionRegistry


class IProviderExtensionRegistry(IExtensionRegistry):
    """ The provider extension registry interface. """

    #### Events ####

    # Fired when a provider has been added to the registry.
    provider_added = Event#(Provider)
    
    # Fired when a provider has been removed from the registry.
    provider_removed = Event#(PluginEvent)
        
    def add_provider(self, provider):
        """ Add an extension provider.

        """

    def get_providers(self):
        """ Return all of the providers in the registry.

        """
        
    def remove_provider(self, provider):
        """ Remove an extension provider.

        Raise a 'ValueError' if the provider is not in the registry.

        """
    
#### EOF ######################################################################
