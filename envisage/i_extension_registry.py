# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The interface for extension registries. """


# Enthought library imports.
from traits.api import Interface


class IExtensionRegistry(Interface):
    """ The interface for extension registries. """

    def add_extension_point_listener(self, listener, extension_point_id=None):
        """ Add a listener for extensions being added or removed.

        A listener is any Python callable with the following signature::

          def listener(extension_registry, extension_point_changed_event):

                ...

        If an extension point is specified then the listener will only be
        called when extensions are added to or removed from that extension
        point (the extension point may or may not have been added to the
        registry at the time of this call).

        If *no* extension point is specified then the listener will be called
        when extensions are added to or removed from *any* extension point.

        When extensions are added or removed all specific listeners are called
        first (in arbitrary order), followed by all non-specific listeners
        (again, in arbitrary order).

        """

    def add_extension_point(self, extension_point):
        """ Add an extension point.

        If an extension point already exists with this Id then it is simply
        replaced.

        """

    def get_extensions(self, extension_point_id):
        """ Return the extensions contributed to an extension point.

        Return an empty list if the extension point does not exist.

        """

    def get_extension_point(self, extension_point_id):
        """ Return the extension point with the specified Id.

        Return None if no such extension point exists.

        """

    def get_extension_points(self):
        """ Return all extension points that have been added to the registry.

        """

    def remove_extension_point_listener(self,listener,extension_point_id=None):
        """ Remove a listener for extensions being added or removed.

        Raise a 'ValueError' if the listener does not exist.

        """

    def remove_extension_point(self, extension_point_id):
        """ Remove an extension point.

        Raise an 'UnknownExtensionPoint' exception if no extension point exists
        with the specified Id.

        """

    def set_extensions(self, extension_point_id, extensions):
        """ Set the extensions contributed to an extension point.

        """

#### EOF ######################################################################
