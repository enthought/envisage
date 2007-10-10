""" The default base class for extension providers. """


# Enthought library imports.
from enthought.traits.api import Event, HasTraits, implements

# Local imports.
from extension_point_changed_event import ExtensionPointChangedEvent
from i_extension_provider import IExtensionProvider


class ExtensionProvider(HasTraits):
    """ The default base class for extension providers. """

    implements(IExtensionProvider)

    #### 'IExtensionProvider' interface #######################################
    
    # The event fired when one of the provider's extension points has changed.
    extension_point_changed = Event(ExtensionPointChangedEvent)

    def get_extension_points(self):
        """ Return the extension points offered by the provider. """

        return []
    
    def get_extensions(self, extension_point):
        """ Return the provider's extensions to an extension point. """

        return []

    ##### Protected 'ExtensionProvider' interface #############################

    def _fire_extension_point_changed(self, extension_point_id, added, removed,
                                      index):
        """ Fire an extension point changed event. """

        self.extension_point_changed = ExtensionPointChangedEvent(
            extension_point_id = extension_point_id,
            added              = added,
            removed            = removed,
            index              = index
        )

        return
    
#### EOF ######################################################################
