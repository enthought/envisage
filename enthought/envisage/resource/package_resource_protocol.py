""" A resource protocol for package resources. """


# Standard library imports.
import pkg_resources

# Enthought library imports.
from enthought.traits.api import HasTraits, implements

# Local imports.
from i_resource_protocol import IResourceProtocol


class PackageResourceProtocol(HasTraits):
    """ A resource protocol for package resources.

    This protocol uses 'pkg_resources' to find and access resources.

    An address for this protocol is a string in the form::

        'package:resource'

    e.g::
    
        'acme.ui.workbench:preferences.init'

        
    """

    implements(IResourceProtocol)
    
    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-object object for the specified address. """

        package, resource_name = address.split(':')

        return pkg_resources.resource_stream(package, resource_name)

#### EOF ######################################################################
