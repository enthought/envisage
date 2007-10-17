""" The provider extension registry interface. """


# Enthought library imports.
from enthought.traits.api import List

# Local imports.
from i_extension_registry import IExtensionRegistry
from i_extension_provider import IExtensionProvider


class IProviderExtensionRegistry(IExtensionRegistry):
    """ The provider extension registry interface. """

    # The extension providers that populate the registry.
    #
    # There is currently no way to express this in traits, but this trait is
    # readonly, meaning that you can use the list to iterate over all of the
    # items in it, and you can listen for changes to the list, but if you want
    # to add or remove a provider you should call 'add_provider' or
    # 'remove_provider' respectively.
    providers = List(IExtensionProvider)
        
    def add_provider(self, provider):
        """ Add an extension provider.

        """

    def remove_provider(self, provider):
        """ Remove an extension provider.

        Raise a 'ValueError' if the provider is not in the registry.

        """
    
#### EOF ######################################################################
