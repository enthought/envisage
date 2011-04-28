""" A resource protocol for HTTP documents. """


# Enthought library imports.
from traits.api import HasTraits, implements

# Local imports.
from i_resource_protocol import IResourceProtocol
from no_such_resource_error import NoSuchResourceError


class HTTPResourceProtocol(HasTraits):
    """ A resource protocol for HTTP documents. """

    implements(IResourceProtocol)

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        # Do the import here 'cos I'm not sure how much this will actually
        # be used.
        import urllib2

        try:
            f = urllib2.urlopen('http://' + address)

        except urllib2.HTTPError:
            raise NoSuchResourceError('http:://' + address)

        return f

#### EOF ######################################################################
