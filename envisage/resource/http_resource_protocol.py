""" A resource protocol for HTTP documents. """

import sys

# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_resource_protocol import IResourceProtocol
from .no_such_resource_error import NoSuchResourceError


@provides(IResourceProtocol)
class HTTPResourceProtocol(HasTraits):
    """ A resource protocol for HTTP documents. """

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        # Do the import here 'cos I'm not sure how much this will actually
        # be used.
        if sys.version_info[0] >= 3:
            from urllib.request import urlopen
            from urllib.error import HTTPError
        else:
            from urllib2 import urlopen, HTTPError

        try:
            f = urlopen('http://' + address)

        except HTTPError:
            raise NoSuchResourceError('http:://' + address)

        return f

#### EOF ######################################################################
