""" A resource protocol for a local file system. """


# Enthought library imports.
from enthought.traits.api import HasTraits, implements

# Local imports.
from i_resource_protocol import IResourceProtocol


class FileResourceProtocol(HasTraits):
    """ A resource protocol for a local file system. """

    implements(IResourceProtocol)
    
    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-object object for the specified address. """

        # Opened in binary mode to be consistent with package resources. This
        # means, for example, that line-endings will not be converted.
        return file(address, 'rb')

#### EOF ######################################################################
