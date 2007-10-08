""" An event fired when a provider's extensions have changed. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits, List, Str


class ExtensionsChangedEvent(HasTraits):
    """ An event fired when a provider's extensions have changed. """

    # The extension point that has changed.
    extension_point = Str

    # The extensions that have been added to the extension point.
    added = List

    # The extensions that have been removed from the extension point.
    removed = List

    # The index at which the first extension was added or removed.
    #
    # The valid values are::
    #
    # 'None' to indicate that no detailed index information is available.
    # An integer that is the index of the first item added/removed.
    # A Python 'slice' object that describes which items were added/removed.
    index = Any
    
#### EOF ######################################################################
