""" The default extension registry implementation. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import List, Property, on_trait_change

# Local imports.
from i_extension_provider import IExtensionProvider
from mutable_extension_registry import MutableExtensionRegistry


# Logging.
logger = logging.getLogger(__name__)


class ExtensionRegistry(MutableExtensionRegistry):
    """ The default extension registry implementation. """

    #### 'ExtensionRegistry' interface ########################################

    # The extension providers that populate the registry.
    providers = Property(List(IExtensionProvider))

    ###########################################################################
    # Private interface.
    ###########################################################################

    # The extension providers that populate the registry.
    _providers = List(IExtensionProvider)

    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def get_extensions(self, extension_point):
        """ Return all contributions to an extension point. """

        self._lk.acquire()
        try:
            self._check_extension_point(extension_point)

            all_extensions = []
            for extensions in self._get_extensions(extension_point):
                all_extensions.extend(extensions)

        finally:
            self._lk.release()

        return all_extensions

    ###########################################################################
    # The following methods are not supported by this implementation.
    # Extensions are added and removed from individual providers instead.
    ###########################################################################
    
    def add_extension(self, extension_point, extension):
        """ Contribute an extension to an extension point. """

        raise NotImplementedError

    def add_extensions(self, extension_point, extensions):
        """ Contribute a list of extensions to an extension point. """

        raise NotImplementedError

    def remove_extension(self, extension_point, extension):
        """ Remove a contribution from an extension point. """

        raise NotImplementedError

    def remove_extensions(self, extension_point, extensions):
        """ Remove a list of contributions from an extension point. """

        raise NotImplementedError

    def set_extensions(self, extension_point, extensions):
        """ Set the extensions to an extension point. """

        raise NotImplementedError

    ###########################################################################
    # 'ExtensionRegistry' interface.
    ###########################################################################

    def _get_providers(self):
        """ Property getter. """

        self._lk.acquire()
        providers = self._providers[:]
        self._lk.release()

        return providers

    def _set_providers(self, providers):
        """ Property setter. """

        self._lk.acquire()
        self._providers = providers
        self._lk.release()

        return
        
    def add_provider(self, provider):
        """ Add an extension provider. """

        self.add_providers([provider])

        return

    def add_providers(self, providers):
        """ Add a list of extension providers. """

        self._lk.acquire()

        events = {}
        for provider in providers:
            self._add_provider(provider, events)

        for extension_point, (added, index) in events.items():
            refs = self._get_listener_refs(extension_point)
            events[extension_point] = (refs, added, index)

        self._lk.release()

        for extension_point, (refs, added, index) in events.items():
            self._call_listeners(refs, extension_point, added, [], index)

        return

    def remove_provider(self, provider):
        """ Remove an extension provider.

        Does nothing if the provider are not present.

        N.B. There is no 'remove_providers' method because we cannot create
        ---- valid list events if non-consecutive providers are removed. Hence
             you have to remove providers one at a time.

        """

        self._lk.acquire()

        events = {}
        self._remove_provider(provider, events)

        for extension_point, (added, index) in events.items():
            refs = self._get_listener_refs(extension_point)
            events[extension_point] = (refs, added, index)

        self._lk.release()

        for extension_point, (refs, removed, index) in events.items():
            self._call_listeners(refs, extension_point, [], removed, index)

        return
    
    ###########################################################################
    # Protected 'ExtensionRegistry' interface.
    ###########################################################################

    def _add_provider(self, provider, events):
        """ Add a new provider. """

        # Does the provider contribute any extensions to an extension point
        # that has already been accessed?
        for extension_point, extensions in self._extensions.items():
            new = provider.get_extensions(extension_point)
            if len(new) > 0:
                if extension_point not in events:
                    index = sum(map(len, extensions))
                    events[extension_point] = (new[:], index)
                    
                else:
                    added, index = events[extension_point]
                    added.extend(new)

            extensions.append(new)
            
        self._providers.append(provider)

        return

    def _remove_provider(self, provider, events):
        """ Remove a provider. """

        if provider in self._providers:
            index = self._providers.index(provider)

            # Does the provider contribute any extensions to an extension point
            # that has already been accessed?
            for extension_point, extensions in self._extensions.items():
                old = extensions[index]
                if len(old) > 0:
                    index = sum(map(len, extensions[:index]))
                    events[extension_point] = (old[:], index)

                del extensions[index]

            self._providers.remove(provider)

        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################
    
    @on_trait_change('_providers.extensions_changed')
    def _providers_extensions_changed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        if trait_name == 'extensions_changed':
            logger.debug('provider <%s> extensions changed', obj)

            extension_point = event.extension_point
            
            self._lk.acquire()
            try:
                index = self._providers.index(obj)
                extensions = self._extensions[extension_point][index]

                if len(event.removed) > 0:
                    # Removed.
                    for extension in event.removed:
                        extensions.remove(extension)
                    
                elif len(event.added) > 0:
                    # Added.
                    extensions.extend(event.added)

                event_index = sum(map(len, self._extensions[extension_point][:index]))
                event_index += event.index


                refs = self._get_listener_refs(extension_point)
                
            finally:
                self._lk.release()

            # Let any listeners know that the extensions have been added.
            self._call_listeners(
                refs, extension_point, event.added, event.removed, index
            )

        return

    #### Methods ##############################################################
    
    def _get_extensions(self, extension_point):
        """ Return the extensions for the given extension point. """

        self._check_extension_point(extension_point)

        # Has this extensin point already been accessed?
        if extension_point in self._extensions:
            extensions = self._extensions[extension_point]

        # If not, then see if any of the providers have any contributions to
        # make.
        else:
            extensions = self._initialize_extensions(extension_point)
            self._extensions[extension_point] = extensions
                
        return extensions
    
    def _initialize_extensions(self, extension_point):
        """ Initialize the extensions to an extension point. """

        extensions = []
        for provider in self._providers:
            contributions = provider.get_extensions(extension_point)[:]
            if not self.strict and len(contributions) > 0:
                self._extension_points[extension_point] = extension_point
            
            extensions.append(contributions)

        logger.debug('extensions to <%s> : <%s>', extension_point, extensions)

        return extensions

#### EOF ######################################################################
