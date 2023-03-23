# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The default base class for extension providers. """


# Enthought library imports.
from traits.api import Event, HasTraits, provides

# Local imports.
from .extension_point_changed_event import ExtensionPointChangedEvent
from .i_extension_provider import IExtensionProvider


@provides(IExtensionProvider)
class ExtensionProvider(HasTraits):
    """The default base class for extension providers."""

    #### 'IExtensionProvider' interface #######################################

    #: The event fired when one of the provider's extension points has been
    #: changed (where 'changed' means that the provider has added or removed
    #: contributions to or from an extension point).
    extension_point_changed = Event(ExtensionPointChangedEvent)

    def get_extension_points(self):
        """Return the extension points offered by the provider."""

        return []

    def get_extensions(self, extension_point_id):
        """Return the provider's extensions to an extension point."""

        return []

    ##### Protected 'ExtensionProvider' interface #############################

    def _fire_extension_point_changed(
        self, extension_point_id, added, removed, index
    ):
        """Fire an extension point changed event."""

        self.extension_point_changed = ExtensionPointChangedEvent(
            extension_point_id=extension_point_id,
            added=added,
            removed=removed,
            index=index,
        )
