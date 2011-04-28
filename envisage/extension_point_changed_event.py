""" An event fired when an extension point's extensions have changed. """


# Enthought library imports.
from traits.api import TraitListEvent


class ExtensionPointChangedEvent(TraitListEvent):
    """ An event fired when an extension point's extensions have changed. """

    def __init__ (self, extension_point_id=None, **kw):
        """ Constructor. """

        # The base class has the 'index', 'removed' and 'added' attributes.
        super(ExtensionPointChangedEvent, self).__init__(**kw)

        # We add the extension point Id.
        self.extension_point_id = extension_point_id

        return

#### EOF ######################################################################
