""" A resource protocol for a local file system. """


# Standard library imports.
import errno

# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_resource_protocol import IResourceProtocol
from .no_such_resource_error import NoSuchResourceError


@provides(IResourceProtocol)
class FileResourceProtocol(HasTraits):
    """ A resource protocol for a local file system. """

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        # Opened in binary mode to be consistent with package resources. This
        # means, for example, that line-endings will not be converted.
        try:
            f = open(address, 'rb')

        except IOError as e:
            if e.errno == errno.ENOENT:
                raise NoSuchResourceError(address)

            else:
                raise

        return f

#### EOF ######################################################################
