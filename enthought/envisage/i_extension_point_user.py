""" The interface for objects that want to declare/access extension points. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface

# Local imports.
from i_extension_registry import IExtensionRegistry


class IExtensionPointUser(Interface):
    """ The interface for objects that want to declare/access extension points.

    """

    # The extension registry that the object's extension points are stored in.
    extension_registry = Instance(IExtensionRegistry)

#### EOF ######################################################################
