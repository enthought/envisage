""" The provider extension registry interface. """



# Local imports.
from .i_extension_registry import IExtensionRegistry


class IProviderExtensionRegistry(IExtensionRegistry):
    """ The provider extension registry interface. """

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
