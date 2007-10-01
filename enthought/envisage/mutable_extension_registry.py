""" A mutable, manually populated extension registry. """


# Standard library imports.
import threading

# Enthought library imports.
from enthought.traits.api import Bool, Dict, HasTraits, implements

# Local imports.
from i_extension_registry import IExtensionRegistry
from safeweakref import ref


class MutableExtensionRegistry(HasTraits):
    """ A mutable, manually populated extension registry. """

    implements(IExtensionRegistry)

    ###########################################################################
    # 'MutableExtensionRegistry' interface.
    ###########################################################################

    # If this is True, then you can't add extensions to an extension point
    # unless the extension point has been explicitly added first (via a call
    # to 'add_extension_point').
    strict = Bool(False)
    
    ###########################################################################
    # Protected 'MutableExtensionRegistry' interface.
    ###########################################################################

    # A dictionary of extensions, keyed by extension point.
    #
    # e.g. Dict(extension_point, [extension])
    #
    # Where 'extension_point' can be any *hashable* object, and 'extension' can
    # be any object.
    _extensions = Dict

    # The extension points that have been added *explicitly*.
    _extension_points = Dict
    
    # Extension listeners.
    #
    # These are called when extensions are added to or removed from an
    # extension point.
    #
    # e.g. Dict(extension_point, [weakref.ref(callable)])
    #
    # Where 'extension_point' can be any *hashable* object, and 'callable' is
    # any Python callable with the following signature:-
    #
    # def listener(extension_registry, extension_point, added, removed, index):
    #     ...
    #
    # 'added' is a list of any extensions that have been added (may be the
    # empty list).
    #
    # 'removed' is a list of any extensions that have been removed (may be the
    # empty list).
    #
    # 'index' is the index of the first item that was added/removed (or the
    # slice for the slice operations).
    _listeners = Dict

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(MutableExtensionRegistry, self).__init__(**traits)

        # A lock to make access to the registry thread-safe.
        self._lk = threading.Lock()

        return
    
    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def add_extension(self, extension_point, extension):
        """ Contribute an extension to an extension point.

        If the extension point has not previously been added to the registry
        then it is added automatically here (unless the registry is in 'strict'
        mode, in which case an exception is raised).
        
        """

        self.add_extensions(extension_point, [extension])

        return

    def add_extensions(self, extension_point, extensions):
        """ Contribute a list of extensions to an extension point.

        If the extension point has not previously been added to the registry
        then it is added automatically here (unless the registry is in 'strict'
        mode, in which case an exception is raised).

        """

        self._lk.acquire()
        try:
            old   = self._get_extensions(extension_point)
            index = len(old)
            old.extend(extensions)

            if not extension_point in self._extension_points:
                self._extension_points[extension_point] = extension_point

            refs = self._get_listener_refs(extension_point)

        finally:
            self._lk.release()
            
        # Let any listeners know that the extensions have been added.
        self._call_listeners(refs, extension_point, extensions, [], index)
        
        return

    def add_extension_listener(self, listener, extension_point=None):
        """ Add a listener for extensions being added or removed.

        If an extension point is specified then the listener will only called
        when extensions are added to or removed from that extension point (the
        extension point may or may not have been added to the registry at the
        time of this call).
        
        If no extension point is specified then the listener will be called
        when extensions are added to or removed from *any* extension point.

        When extensions are added or removed all specific listeners are called
        (in arbitrary order), followed by all non-specific listeners (again, in
        arbitrary order).
        
        """

        self._lk.acquire()
        listeners = self._listeners.setdefault(extension_point, [])
        listeners.append(ref(listener))
        self._lk.release()

        return

    def add_extension_point(self, extension_point):
        """ Add an extension point. """

        self._lk.acquire()
        self._extension_points[extension_point] = None
        self._lk.release()

        return

    def get_extensions(self, extension_point, **kw):
        """ Return all contributions to an extension point.

        Returns an empty list if the extension point does not exist.

        """

        self._lk.acquire()
        try:
            extensions = self._get_extensions(extension_point)[:]

        finally:
            self._lk.release()

        return extensions

    def get_extension_points(self):
        """ Return all extension points. """

        self._lk.acquire()
        extension_points = self._extension_points.keys()
        self._lk.release()

        return extension_points
    
    def remove_extension(self, extension_point, extension):
        """ Remove a contribution from an extension point.

        Raises a 'ValueError' if the extension does not exist.

        """

        self._lk.acquire()
        try:
            extensions = self._get_extensions(extension_point)
            index = extensions.index(extension)
            extensions.remove(extension)

            refs = self._get_listener_refs(extension_point)

        finally:
            self._lk.release()
            
        # Let any listeners know that the extension has been removed.
        self._call_listeners(refs, extension_point, [], [extension], index)

        return

    def remove_extensions(self, extension_point, extensions):
        """ Remove a list of contributions from an extension point.

        Raises a 'ValueError' if any of the extensions does not exist.
        
        """

        self._lk.acquire()
        try:
            for extension in extensions:
                extensions = self._extensions.setdefault(extension_point, [])
                extensions.remove(extension)

            refs = self._get_listener_refs(extension_point)

        finally:
            self._lk.release()

        # Let any listeners know that the extensions have been removed.
        self._call_listeners(refs, extension_point, [], extensions, -1)

        return

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
            del self._extension_points[extension_point]

            # Remove any extensions to the extension point.
            if extension_point in self._extensions:
                del self._extensions[extension_point]

        finally:
            self._lk.release()
        
        return

    def set_extensions(self, extension_point, extensions):
        """ Set the extensions to an extension point. """

        self._lk.acquire()
        try:
            old = self._get_extensions(extension_point)
            self._extensions[extension_point] = extensions

            refs = self._get_listener_refs(extension_point)

        finally:
            self._lk.release()

        # Let any listeners know that the extensions have been set.
        self._call_listeners(refs, extension_point, extensions, old, -1)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _call_listeners(self, refs, extension_point, added, removed, index):
        """ Call listeners that are listening to an extension point.

        We call those listeners that are listening to this extension point
        specifically first, followed by those that are listening to any
        extension point.

        """

        for ref in refs:
            listener = ref()
            if listener is not None:
                listener(self, extension_point, added, removed, index)

        return

    def _check_extension_point(self, extension_point):
        """ Check to see if the extension point exists. """
        
        if self.strict and not extension_point in self._extension_points:
            raise ValueError('unknown extension point <%s>' % extension_point)

        return
    
    def _get_extensions(self, extension_point):
        """ Return the extensions for the given extension point. """

        self._check_extension_point(extension_point)
        
        return self._extensions.setdefault(extension_point, [])
    
    def _get_listener_refs(self, extension_point):
        """ Get the weak references to all listeners for an extension point.

        Returns a list containing the weak references to those listeners that
        are listening to this extension point specifically first, followed by
        those that are listening to any extension point.

        """

        refs = []
        refs.extend(self._listeners.get(extension_point, []))
        refs.extend(self._listeners.get(None, []))

        return refs
    
#### EOF ######################################################################
