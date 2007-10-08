""" A base class for extension registry implementation. """


# Standard library imports.
import logging, threading

# Enthought library imports.
from enthought.traits.api import Dict, HasTraits, implements

# Local imports.
from extension_point_changed_event import ExtensionPointChangedEvent
from i_extension_registry import IExtensionRegistry
import safeweakref
from unknown_extension_point import UnknownExtensionPoint


# Logging.
logger = logging.getLogger(__name__)


class ExtensionRegistry(HasTraits):
    """ A base class for extension registry implementation. """

    implements(IExtensionRegistry)

    ###########################################################################
    # Protected 'ExtensionRegistry' interface.
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
    # def listener(extension_registry, extension_point_changed_event):
    #     ...
    _listeners = Dict

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        # A lock to make access to the registry thread-safe.
        self._lk = threading.Lock()

        # We have to create the lock first in-case it is required when a trait
        # is set.
        super(ExtensionRegistry, self).__init__(**traits)

        return
    
    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def add_extension_listener(self, listener, extension_point_id=None):
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
        listeners = self._listeners.setdefault(extension_point_id, [])
        listeners.append(safeweakref.ref(listener))
        self._lk.release()

        return

    def add_extension_point(self, extension_point):
        """ Add an extension point. """

        self._lk.acquire()
        self._extension_points[extension_point.id] = extension_point
        self._lk.release()

        logger.debug('extension point <%s> added', extension_point.id)
        
        return

    def get_extensions(self, extension_point_id, **kw):
        """ Return all contributions to an extension point.

        Returns an empty list if the extension point does not exist.

        """

        self._lk.acquire()
        try:
            extensions = self._get_extensions(extension_point_id)[:]

        finally:
            self._lk.release()

        return extensions

    def get_extension_points(self):
        """ Return all extension points. """

        self._lk.acquire()
        extension_points = self._extension_points.values()
        self._lk.release()

        return extension_points

    def remove_extension_listener(self, listener, extension_point_id=None):
        """ Remove a listener for extensions being added/removed.

        Raise a 'ValueError' if the listener does not exist.

        """

        self._lk.acquire()
        try:
            listeners = self._listeners.setdefault(extension_point_id, [])
            listeners.remove(safeweakref.ref(listener))

        finally:
            self._lk.release()

        return

    def remove_extension_point(self, extension_point_id):
        """ Remove an extension point.

        Raise an 'UnknownExtensionPoint' exception if the extension point does
        not exist.

        """

        self._lk.acquire()
        try:
            self._check_extension_point(extension_point_id)

            # Remove the extension point.
            del self._extension_points[extension_point_id]

            # Remove any extensions to the extension point.
            if extension_point_id in self._extensions:
                del self._extensions[extension_point_id]

            logger.debug('extension point <%s> removed', extension_point_id)

        finally:
            self._lk.release()
        
        return

    ###########################################################################
    # Protected 'ExtensionRegistry' interface.
    ###########################################################################

    def _call_listeners(self, refs, extension_point_id, added, removed, index):
        """ Call listeners that are listening to an extension point. """

        event = ExtensionPointChangedEvent(
            extension_point_id = extension_point_id,
            added              = added,
            removed            = removed,
            index              = index
        )

        for ref in refs:
            listener = ref()
            if listener is not None:
                listener(self, event)

        return

    def _check_extension_point(self, extension_point_id):
        """ Check to see if the extension point exists. """
        
        if not extension_point_id in self._extension_points:
            raise UnknownExtensionPoint(extension_point_id)

        return

    def _get_extensions(self, extension_point_id):
        """ Return the extensions for the given extension point. """

        return self._extensions.setdefault(extension_point_id, [])

    def _get_listener_refs(self, extension_point_id):
        """ Get weak references to all listeners for an extension point.

        Returns a list containing the weak references to those listeners that
        are listening to this extension point specifically first, followed by
        those that are listening to any extension point.

        """

        refs = []
        refs.extend(self._listeners.get(extension_point_id, []))
        refs.extend(self._listeners.get(None, []))

        return refs

#### EOF ######################################################################
