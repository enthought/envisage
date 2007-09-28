""" An event fired when a providers extensions have changed. """


# Enthought library imports.
from enthought.traits.api import HasTraits, List, Str


class ExtensionsChangedEvent(HasTraits):
    """ An event fired when a providers extensions have changed. """

    # The extension point that has changed.
    extension_point = Str

    # The extensions that have been added to the extension point.
    added = List

    # The extensions that have been removed from the extension point.
    removed = List
    
#### EOF ######################################################################
