""" A resource protocol for a local file system. """


# Standard library imports.
import errno

# Enthought library imports.
from traits.api import HasTraits, implements

# Local imports.
from i_resource_protocol import IResourceProtocol
from no_such_resource_error import NoSuchResourceError


class FileResourceProtocol(HasTraits):
    """ A resource protocol for a local file system. """

    implements(IResourceProtocol)

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        # Opened in binary mode to be consistent with package resources. This
        # means, for example, that line-endings will not be converted.
        try:
            f = file(address, 'rb')

        except IOError, e:
            if e.errno == errno.ENOENT:
                raise NoSuchResourceError(address)

            else:
                raise

        return f

#### EOF ######################################################################
