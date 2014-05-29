""" The interface for extension providers. """


# Enthought library imports.
from traits.api import Event, Interface

# Local imports.
from .extension_point_changed_event import ExtensionPointChangedEvent


class IExtensionProvider(Interface):
    """ The interface for extension providers. """

    # The event fired when one of the provider's extension points has changed.
    extension_point_changed = Event(ExtensionPointChangedEvent)

    def get_extension_points(self):
        """ Return the extension points offered by the provider.

        Return an empty list if the provider does not offer any extension
        points.

        """

    def get_extensions(self, extension_point_id):
        """ Return the provider's extensions to an extension point.

        The return value *must* be a list. Return an empty list if the provider
        does not contribute any extensions to the extension point.

        """

#### EOF ######################################################################
