""" An event fired when an extension point's extensions have changed. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits, List, Str


class ExtensionPointChangedEvent(HasTraits):
    """ An event fired when an extension point's extensions have changed. """
    
    # The Id of the extension point that changed.
    extension_point_id = Str

    # The extensions that have been added to the extension point.
    added = List

    # The extensions that have been removed from the extension point.
    removed = List

    # The index at which the first extension was added or removed.
    index = Any
    
#### EOF ######################################################################
