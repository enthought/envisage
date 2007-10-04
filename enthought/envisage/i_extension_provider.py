""" The interface for extension providers. """


# Enthought library imports.
from enthought.traits.api import Event, Interface

# Local imports.
from extensions_changed_event import ExtensionsChangedEvent


class IExtensionProvider(Interface):
    """ The interface for extension providers. """

    # The event fired when the provider's extensions have changed.
    extensions_changed = Event(ExtensionsChangedEvent)
    
    def get_extension_points(self):
        """ Return the extension points offered by the provider.

        Return an empty list if the provider does not offer any extension
        points.

        """

    def get_extensions(self, extension_point):
        """ Return the provider's extensions to an extension point.

        The return value *must* be a list. Return an empty list if the provider
        does not contribute any extensions to the extension point.

        """

#### EOF ######################################################################
