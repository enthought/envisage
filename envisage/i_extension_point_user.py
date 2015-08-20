""" The interface for objects using the 'ExtensionPoint' trait type. """


# Enthought library imports.
from traits.api import Instance, Interface

# Local imports.
from .i_extension_registry import IExtensionRegistry


class IExtensionPointUser(Interface):
    """ The interface for objects using the 'ExtensionPoint' trait type. """

    # The extension registry that the object's extension points are stored in.
    extension_registry = Instance(IExtensionRegistry)

#### EOF ######################################################################
