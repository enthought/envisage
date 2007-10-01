""" The default extension registry implementation. """


# Standard library imports.
import logging, threading

# Enthought library imports.
from enthought.traits.api import Bool, Dict, HasTraits, List, Property
from enthought.traits.api import implements, on_trait_change

# Local imports.
from i_extension_registry import IExtensionRegistry
from i_extension_provider import IExtensionProvider
from safeweakref import ref


# Logging.
logger = logging.getLogger(__name__)


class ExtensionRegistry(HasTraits):
    """ The default extension registry implementation. """

    implements(IExtensionRegistry)
    
    #### 'ExtensionRegistry' interface ########################################

    # The extension providers that populate the registry.
    providers = Property(List(IExtensionProvider))

    # If this is True, then you can't add extensions to an extension point
    # unless the extension point has been explicitly added first (via a call to
    # 'add_extension_point').
    strict = Bool(False)

    ###########################################################################
    # Private interface.
    ###########################################################################

    # A dictionary of extensions, keyed by extension point.
    #
    # e.g. Dict(extension_point, [[extension]])
    #
    # Where 'extension_point' can be any *hashable* object, and 'extension' can
    # be any object.
    _extensions = Dict

    # The explicitly added extension points.
    _extension_points = Dict
    
    # Extension listeners.
    #
    # These are called when extensions are added to or removed from extension
    # points.
    #
    # e.g. Dict(extension_point, [weakref.ref(callable)])
    #
    # Where 'extension_point' can be any *hashable* object, and 'callable' is
    # any Python callable with the following signature:-
    #
    # def listener(extension_registry, extension_point, added, removed):
    #     ...
    #
    # 'added' is a list of any extensions that have been added (may be the
    # empty list).
    #
    # 'removed' is a list of any extensions that have been removed (may be the
    # empty list).
    _listeners = Dict

    # The extension providers that populate the registry.
    _providers = List(IExtensionProvider)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        # A lock to make access to the registry thread-safe.
        self._lk = threading.Lock()

        super(ExtensionRegistry, self).__init__(**traits)

        return
    
    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def add_extension(self, extension_point, extension):
        """ Contribute an extension to an extension point. """

        raise NotImplementedError

    def add_extensions(self, extension_point, extensions):
        """ Contribute a list of extensions to an extension point. """

        raise NotImplementedError

    def add_extension_listener(self, listener, extension_point=None):
        """ Add a listener for extensions being added or removed. """

        self._lk.acquire()
        listeners = self._listeners.setdefault(extension_point, [])
        listeners.append(ref(listener))
        self._lk.release()

        return

    def add_extension_point(self, extension_point):
        """ Add an extension point. """

        self._lk.acquire()
        self._extension_points[extension_point] = extension_point
        self._lk.release()

        return

    def get_extensions(self, extension_point, **kw):
        """ Return all contributions to an extension point. """

        self._lk.acquire()
        try:
            self._check_extension_point(extension_point)

            all_extensions = []
            for extensions in self._get_extensions(extension_point, **kw):
                all_extensions.extend(extensions)

        finally:
            self._lk.release()

        return all_extensions

    def get_extension_points(self):
        """ Return all extension points. """

        self._lk.acquire()
        extension_points = self._extension_points.keys()
        self._lk.release()

        return extension_points
    
    def remove_extension(self, extension_point, extension):
        """ Remove a contribution from an extension point. """

        raise NotImplementedError

    def remove_extensions(self, extension_point, extensions):
        """ Remove a list of contributions from an extension point. """

        raise NotImplementedError

    def remove_extension_listener(self, listener, extension_point=None):
        """ Remove a listener for extensions being added/removed.

        Raises a 'ValueError' if the listener does not exist.

        """

        self._lk.acquire()
        try:
            listeners = self._listeners.setdefault(extension_point, [])
            listeners.remove(ref(listener))

        finally:
            self._lk.release()

        return

    def remove_extension_point(self, extension_point):
        """ Remove an extension point.

        Raises a 'KeyError' if the extension point does not exist.

        """

        self._lk.acquire()
        try:
            self._check_extension_point()
            del self._extension_points[extension_point]

            if extension_point in self._extensions:
                del self._extensions[extension_point]
                
        finally:
            self._lk.release()
        
        return

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
        self._lk.release()

        for extension_point, (added, index) in events.items():
            self._call_listeners(extension_point, added, [], index)

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

        self._lk.release()

        for extension_point, (removed, index) in events.items():
            self._call_listeners(extension_point, [], removed, index)

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

            finally:
                self._lk.release()

            # Let any listeners know that the extensions have been added.
            self._call_listeners(
                extension_point, event.added, event.removed, index
            )

        return

    #### Methods ##############################################################

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
    
    def _call_listeners(self, extension_point, added, removed, index):
        """ Call listeners that are listening to an extension point.

        We call those listeners that are listening to this extension point
        specifically first, followed by those that are listening to any
        extension point.

        """

        for ref in self._get_listener_refs(extension_point):
            listener = ref()
            if listener is not None:
                listener(self, extension_point, added, removed, index)

        return

    def _check_extension_point(self, extension_point):
        """ Check to see if the extension point exists. """

        if not extension_point in self._extension_points:
            if self.strict:
                message = 'no such extension point <%s>' % extension_point
                raise ValueError(message)

            else:
                self._extension_points[extension_point] = extension_point

        return
    
    def _get_extensions(self, extension_point, **kw):
        """ Return the extensions for the given extension point. """

        try:
            extensions = self._extensions[extension_point]
            
        except KeyError:
            extensions = self._initialize_extensions(extension_point)
            self._extensions[extension_point] = extensions
            
        return extensions
    
    def _get_listener_refs(self, extension_point):
        """ Get the weak references to all listeners for an extension point.

        Returns a list containing the weak references to those listeners that
        are listening to this extension point specifically first, followed by
        those that are listening to any extension point.

        """

        refs = []

        self._lk.acquire()
        refs.extend(self._listeners.get(extension_point, []))
        refs.extend(self._listeners.get(None, []))
        self._lk.release()

        return refs

    def _initialize_extensions(self, extension_point):
        """ Initialize the extensions to an extension point. """

        extensions = []
        for provider in self._providers:
            extensions.append(provider.get_extensions(extension_point)[:])

        logger.debug('extensions to <%s> : <%s>', extension_point, extensions)

        return extensions

#### EOF ######################################################################
