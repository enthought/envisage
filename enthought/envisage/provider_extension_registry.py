""" An extension registry implementation with multiple providers. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import List, Property, on_trait_change

# Local imports.
from extension_registry import ExtensionRegistry
from i_extension_provider import IExtensionProvider


# Logging.
logger = logging.getLogger(__name__)


class ProviderExtensionRegistry(ExtensionRegistry):
    """ An extension registry implementation with multiple providers. """

    #### 'ProviderExtensionRegistry' interface ################################

    # The extension providers that populate the registry.
    providers = Property(List(IExtensionProvider))

    ###########################################################################
    # Private interface.
    ###########################################################################

    # The extension providers that populate the registry.
    _providers = List(IExtensionProvider)

    ###########################################################################
    # Protected 'ExtensionRegistry' interface.
    ###########################################################################

    def _get_extensions(self, extension_point):
        """ Return the extensions for the given extension point. """

        # Has this extension point already been accessed?
        if extension_point in self._extensions:
            extensions = self._extensions[extension_point]

        # If not, then see if any of the providers have any contributions to
        # make.
        else:
            extensions = self._initialize_extensions(extension_point)
            self._extensions[extension_point] = extensions

        all = []
        for extensions in extensions:
            all.extend(extensions)
                
        return all

    ###########################################################################
    # 'ProviderExtensionRegistry' interface.
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

        # Each provider can contribute to multiple extension points, so we
        # build up a dictionary of the 'ExtensionPointChanged' events that we
        # need to fire.
        events = {}
        for provider in providers:
            self._add_provider(provider, events)

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

        # Each provider can contribute to multiple extension points, so we
        # build up a dictionary of the 'ExtensionPointChanged' events that we
        # need to fire.
        events = {}
        self._remove_provider(provider, events)
        
        self._lk.release()

        for extension_point, (refs, removed, index) in events.items():
            self._call_listeners(refs, extension_point, [], removed, index)

        return
    
    ###########################################################################
    # Protected 'ProviderExtensionRegistry' interface.
    ###########################################################################

    def _add_provider(self, provider, events):
        """ Add a new provider. """

        # Add the provider's extension points.
        for extension_point in provider.get_extension_points():
            self._extension_points[extension_point.id] = extension_point
            
        # Does the provider contribute any extensions to an extension point
        # that has already been accessed?
        for extension_point, extensions in self._extensions.items():
            new = provider.get_extensions(extension_point)
            if len(new) > 0:
                if extension_point not in events:
                    index = sum(map(len, extensions))
                    refs  = self._get_listener_refs(extension_point)
                    events[extension_point] = (refs, new[:], index)
                    
                else:
                    added, index, refs = events[extension_point]
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
                    refs  = self._get_listener_refs(extension_point)
                    events[extension_point] = (refs, old[:], index)

                del extensions[index]

            self._providers.remove(provider)

            # Remove the provider's extension points.
            for extension_point in provider.get_extension_points():
                # Remove the extension point.
                del self._extension_points[extension_point_id]

                # Remove any extensions to the extension point.
                if extension_point_id in self._extensions:
                    del self._extensions[extension_point_id]

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################
    
    @on_trait_change('_providers.extension_point_changed')
    def _providers_extension_point_changed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        if trait_name == 'extension_point_changed':
            logger.debug('provider <%s> extension point changed', obj)

            extension_point_id = event.extension_point_id
            
            self._lk.acquire()
            try:
                index = self._providers.index(obj)
                extensions = self._extensions[extension_point_id][index]

                if len(event.removed) > 0:
                    # Removed.
                    for extension in event.removed:
                        extensions.remove(extension)
                    
                elif len(event.added) > 0:
                    # Added.
                    extensions.extend(event.added)

                event_index = sum(
                    map(len, self._extensions[extension_point_id][:index])
                )
                event_index += event.index


                refs = self._get_listener_refs(extension_point_id)
                
            finally:
                self._lk.release()

            # Let any listeners know that the extensions have been added.
            self._call_listeners(
                refs, extension_point_id, event.added, event.removed, index
            )

        return

    #### Methods ##############################################################
    
    def _initialize_extensions(self, extension_point_id):
        """ Initialize the extensions to an extension point. """

        extensions = []
        for provider in self._providers:
            extensions.append(provider.get_extensions(extension_point_id)[:])

        logger.debug('extensions to <%s>:<%s>', extension_point_id, extensions)

        return extensions

#### EOF ######################################################################
