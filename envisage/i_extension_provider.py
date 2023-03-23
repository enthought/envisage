# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The interface for extension providers. """


# Enthought library imports.
from traits.api import Event, Interface

# Local imports.
from .extension_point_changed_event import ExtensionPointChangedEvent


class IExtensionProvider(Interface):
    """The interface for extension providers."""

    # The event fired when one of the provider's extension points has changed.
    extension_point_changed = Event(ExtensionPointChangedEvent)

    def get_extension_points(self):
        """Return the extension points offered by the provider.

        Return an empty list if the provider does not offer any extension
        points.

        """

    def get_extensions(self, extension_point_id):
        """Return the provider's extensions to an extension point.

        The return value *must* be a list. Return an empty list if the provider
        does not contribute any extensions to the extension point.

        """
