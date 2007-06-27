""" The interface for extension registries. """


# Enthought library imports.
from enthought.traits.api import Interface


class IExtensionRegistry(Interface):
    """ The interface for extension registries. """

    def get_extensions(self, extension_point):
        """ Return a list containing all contributions to an extension point.

        Return an empty list if the extension point does not exist.

        """
                        
#### EOF ######################################################################
