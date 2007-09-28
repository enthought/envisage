""" The default base class for extension providers. """


# Enthought library imports.
from enthought.traits.api import Event, HasTraits, implements

# Local imports.
from extensions_changed_event import ExtensionsChangedEvent
from i_extension_provider import IExtensionProvider


class ExtensionProvider(HasTraits):
    """ The default base class for extension providers. """

    implements(IExtensionProvider)

    #### 'IExtensionProvider' interface #######################################
    
    # The event fired when the provider's extensions have changed.
    extensions_changed = Event(ExtensionsChangedEvent)

    def get_extension_points(self):
        """ Return the extension points offered by the provider. """

        return []
    
    def get_extensions(self, extension_point):
        """ Return the provider's extensions to an extension point. """

        return []
    
#### EOF ######################################################################
