""" The interface for mutable extension registries. """


# Enthought library imports.
from enthought.traits.api import Interface

# Local imports.
from i_extension_registry import IExtensionRegistry


class IMutableExtensionRegistry(IExtensionRegistry):
    """ The interface for mutable extension registries.

    This interface just adds methods to add, remove and set the extensions for
    an extension point.

    """

    def add_extension(self, extension_point_id, extension):
        """ Contribute an extension to an extension point.

        Raise an 'UnknownExtensionPoint' exception if no extension point exists
        with the specified Id.

        """

    def add_extensions(self, extension_point_id, extensions):
        """ Contriobute a list of extensions to an extension point.

        Raise an 'UnknownExtensionPoint' exception if no extension point exists
        with the specified Id.

        """

    def remove_extension(self, extension_point_id, extension):
        """ Remove a contribution from an extension point.

        Raise an 'UnknownExtension' exception if the extension does not exist.

        """

    def remove_extensions(self, extension_point_id, extensions):
        """ Remove a list of contributions from an extension point.

        Raise an 'UnknownExtension' exception if any of the extensions does not
        exist.
        
        """

    def set_extensions(self, extension_point_id, extensions):
        """ Set the extensions to an extension point.

        """

#### EOF ######################################################################
