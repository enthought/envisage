""" A resource protocol for HTTP documents. """


# Enthought library imports.
from enthought.traits.api import HasTraits, implements

# Local imports.
from i_resource_protocol import IResourceProtocol


class HTTPResourceProtocol(HasTraits):
    """ A resource protocol for HTTP documents. """

    implements(IResourceProtocol)
    
    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-object object for the specified address. """

        # Do the import here 'cos I'm not sure how much this will actually
        # be used.
        import urllib

        return urllib.urlopen('http://' + address)

#### EOF ######################################################################
