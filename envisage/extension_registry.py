# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A base class for extension registry implementation. """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import Dict, HasTraits, provides

# Local imports.
from .extension_point_changed_event import ExtensionPointChangedEvent
from .i_extension_registry import IExtensionRegistry
from . import safeweakref
from .unknown_extension_point import UnknownExtensionPoint


# Logging.
logger = logging.getLogger(__name__)


@provides(IExtensionRegistry)
class ExtensionRegistry(HasTraits):
    """ A base class for extension registry implementation. """

    ###########################################################################
    # Protected 'ExtensionRegistry' interface.
    ###########################################################################

    # A dictionary of extensions, keyed by extension point.
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
    # A listener is any Python callable with the following signature:-
    #
    # def listener(extension_registry, extension_point_changed_event):
    #     ...
    _listeners = Dict

    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def add_extension_point_listener(self, listener, extension_point_id=None):
        """ Add a listener for extensions being added or removed. """

        listeners = self._listeners.setdefault(extension_point_id, [])
        listeners.append(safeweakref.ref(listener))

        return

    def add_extension_point(self, extension_point):
        """ Add an extension point. """

        self._extension_points[extension_point.id] = extension_point
        logger.debug('extension point <%s> added', extension_point.id)

        return

    def get_extensions(self, extension_point_id):
        """ Return the extensions contributed to an extension point. """

        return self._get_extensions(extension_point_id)[:]

    def get_extension_point(self, extension_point_id):
        """ Return the extension point with the specified Id. """

        return self._extension_points.get(extension_point_id)

    def get_extension_points(self):
        """ Return all extension points. """

        return list(self._extension_points.values())

    def remove_extension_point_listener(self,listener,extension_point_id=None):
        """ Remove a listener for extensions being added or removed. """

        listeners = self._listeners.setdefault(extension_point_id, [])
        listeners.remove(safeweakref.ref(listener))

        return

    def remove_extension_point(self, extension_point_id):
        """ Remove an extension point. """

        self._check_extension_point(extension_point_id)

        # Remove the extension point.
        del self._extension_points[extension_point_id]

        # Remove any extensions to the extension point.
        if extension_point_id in self._extensions:
            old = self._extensions[extension_point_id]
            del self._extensions[extension_point_id]

        else:
            old = []

        refs = self._get_listener_refs(extension_point_id)
        self._call_listeners(refs, extension_point_id, [], old, 0)

        logger.debug('extension point <%s> removed', extension_point_id)

        return

    def set_extensions(self, extension_point_id, extensions):
        """ Set the extensions contributed to an extension point. """

        self._check_extension_point(extension_point_id)

        old = self._get_extensions(extension_point_id)
        self._extensions[extension_point_id] = extensions

        refs = self._get_listener_refs(extension_point_id)
        self._call_listeners(refs, extension_point_id, extensions, old, None)

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
        """ Check to see if the extension point exists.

        Raise an 'UnknownExtensionPoint' if it does not.

        """

        if not extension_point_id in self._extension_points:
            raise UnknownExtensionPoint(extension_point_id)

        return

    def _get_extensions(self, extension_point_id):
        """ Return the extensions for the given extension point. """

        return self._extensions.setdefault(extension_point_id, [])

    def _get_listener_refs(self, extension_point_id):
        """ Get weak references to all listeners to an extension point.

        Returns a list containing the weak references to those listeners that
        are listening to this extension point specifically first, followed by
        those that are listening to any extension point.

        """

        refs = []
        refs.extend(self._listeners.get(extension_point_id, []))
        refs.extend(self._listeners.get(None, []))

        return refs

#### EOF ######################################################################
