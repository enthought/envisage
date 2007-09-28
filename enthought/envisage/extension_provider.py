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

    ##### Protected 'ExtensionProvider' interface #############################

    def _fire_extensions_changed(self, extension_point, added, removed):
        """ Fire an extensions changed event. """

        self.extensions_changed = ExtensionsChangedEvent(
            extension_point=extension_point, added=added, removed=removed
        )

        return
    
#### EOF ######################################################################
