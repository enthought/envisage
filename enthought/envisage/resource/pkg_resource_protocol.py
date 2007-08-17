""" A resource protocol for resources in eggs. """


# Standard library imports.
import pkg_resources

# Enthought library imports.
from enthought.traits.api import HasTraits, implements

# Local imports.
from i_resource_protocol import IResourceProtocol


class PkgResourceProtocol(HasTraits):
    """ A resource protocol for resources in eggs. """

    implements(IResourceProtocol)
    
    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-object object for the specified address. """

        package, resource_name = address.split(':')

        return pkg_resources.resource_stream(package, resource_name)

#### EOF ######################################################################
