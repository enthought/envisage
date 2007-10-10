""" An extension registry implementation with multiple providers. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import List, on_trait_change

# Local imports.
from extension_registry import ExtensionRegistry
from i_extension_provider import IExtensionProvider


# Logging.
logger = logging.getLogger(__name__)


class ProviderExtensionRegistry(ExtensionRegistry):
    """ An extension registry implementation with multiple providers. """

    ####  Private interface ###################################################

    # The extension providers that populate the registry.
    _providers = List(IExtensionProvider)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, providers=None, **traits):
        """ Constructor. """

        super(ProviderExtensionRegistry, self).__init__(**traits)
        
        # This constructor exists because we want the caller to be able to
        # pass in a list of providers at creation time, but we don't that list
        # to be public, and we don't want the caller to be able to modify the
        # list dynamically.
        if providers is not None:
            for provider in providers:
                self._add_provider(provider, {})
            
        return
    
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
        
    def add_provider(self, provider):
        """ Add an extension provider. """

        self._lk.acquire()

        # Each provider can contribute to multiple extension points, so we
        # build up a dictionary of the 'ExtensionPointChanged' events that we
        # need to fire.
        events = {}
        self._add_provider(provider, events)

        self._lk.release()

        for extension_point_id, (refs, added, index) in events.items():
            self._call_listeners(refs, extension_point_id, added, [], index)

        return

    def remove_provider(self, provider):
        """ Remove an extension provider.

        Does nothing if the provider is not present.

        """

        self._lk.acquire()

        # Each provider can contribute to multiple extension points, so we
        # build up a dictionary of the 'ExtensionPointChanged' events that we
        # need to fire.
        events = {}
        self._remove_provider(provider, events)
        
        self._lk.release()

        for extension_point_id, (refs, removed, index) in events.items():
            self._call_listeners(refs, extension_point_id, [], removed, index)

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
                # This is a list of lists, each inner list contains the
                # contributions made to the extension point by a single
                # provider.
                extensions = self._extensions[extension_point_id]
                
                # Find the index of the provider in the provider list. Its
                # contributions are at the same index in the extensions list of
                # lists.
                provider_index = self._providers.index(obj)
                
                # Update the provider's contributions based on the event.
                self._update_list(extensions[provider_index], event)

                # Trnaslate the index from one that refers to the list of
                # contributions from the provider, to the list of contributions
                # from all providers.
                start = sum(map(len, extensions[:provider_index]))
                if isinstance(event.index, slice):
                    event.index = slice(
                        event.index.start + start,
                        event.index.stop  + start,
                        event.index.step
                    )

                else:
                    event.index = event.index + start

                # Find out who is listening.
                refs = self._get_listener_refs(extension_point_id)

            finally:
                self._lk.release()

            # Let any listeners know that the extensions have been added.
            self._call_listeners(
                refs, extension_point_id, event.added, event.removed,
                event.index
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

    def _update_list(self, l, event):
        """ Update a list 'l'  based on an 'ExtensionPointChanged' event. """

        # If nothing was added then this is a 'del' or 'remove' operation.
        if len(event.added) == 0:
            if isinstance(event.index, slice):
                del l[event.index]
                
            else:
                del l[event.index : event.index + len(event.removed)]

        # If nothing was removed then it is an 'append', 'insert' or 'extend'
        # operation.
        elif len(event.removed) == 0:
            if isinstance(event.index, slice):
                # fixme: For some reason, if the index is a slice then the
                # trait list event 'added' trait contains a list of lists?!?
                l[event.index] = event.added#[0]

            else:
                l.insert(event.index, event.added[0])
        
        # Otherwise, it is an assigment ('sort' and 'reverse' fall into this
        # category).
        else:
            if isinstance(event.index, slice):
                # fixme: For some reason, if the index is a slice then the
                # trait list event 'added' trait contains a list of lists?!?
                l[event.index] = event.added#[0]

            else:
                l[event.index : event.index + len(event.added)] = event.added 

        return

#### EOF ######################################################################
