""" An event fired when a provider's extensions have changed. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Int, List, Str


class ExtensionsChangedEvent(HasTraits):
    """ An event fired when a provider's extensions have changed. """

    # The extension point that has changed.
    extension_point = Str

    # The extensions that have been added to the extension point.
    added = List

    # The extensions that have been removed from the extension point.
    removed = List

    # The index at which the first extension was added or removed.
    index = Int
    
#### EOF ######################################################################
