""" The default extension registry implementation. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Instance, List, on_trait_change

# Local imports.
from i_extension_provider import IExtensionProvider
from mutable_extension_registry import MutableExtensionRegistry


# Logging.
logger = logging.getLogger(__name__)


class ExtensionRegistry(MutableExtensionRegistry):
    """ The default extension registry implementation. """

    #### 'ExtensionRegistry' interface ########################################

    # The extension providers that populate the registry.
    providers = List(IExtensionProvider)
    
    ###########################################################################
    # Protected 'MutableExtensionRegistry' interface.
    ###########################################################################

    def _initialize_extensions(self, extension_point):
        """ Initialize the extensions to an extension point. """

        self._check_extension_point(extension_point)
        
        extensions = []
        for provider in self.providers:
            extensions.extend(provider.get_extensions(extension_point))

        logger.debug('extensions to <%s> : <%s>', extension_point, extensions)

        return extensions

    ###########################################################################
    # Private interface.
    ###########################################################################

    @on_trait_change('providers.extensions_changed')
    def _providers_extensions_changed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        if trait_name == 'extensions_changed':
            logger.debug('provider <%s> extensions changed', obj)

            self.remove_extensions(event.extension_point, event.removed)
            self.add_extensions(event.extension_point, event.added)

        return

#### EOF ######################################################################
