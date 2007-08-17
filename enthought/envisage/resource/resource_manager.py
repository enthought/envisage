""" The default resource manager. """



# Enthought library imports.
from enthought.traits.api import Dict, HasTraits, Str, implements

# Local imports.
from i_resource_manager import IResourceManager
from i_resource_protocol import IResourceProtocol

class ResourceManager(HasTraits):
    """ The default resource manager. """

    implements(IResourceManager)

    #### 'IResourceManager' interface #########################################
    
    # The protocols used by the manager to resolve resource URLs.
    resource_protocols = Dict(Str, IResourceProtocol)

    ###########################################################################
    # 'IResourceManager' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _resource_protocols_default(self):
        """ Trait initializer. """

        # We do the import(s) here in case somebody wants a resource manager
        # that doesn't use the default protocol(s).
        from pkg_resource_protocol import PkgResourceProtocol

        # Currently, not such a big set of protocols ;^)
        return {'pkg_resource' : PkgResourceProtocol()}

    #### Methods ##############################################################

    def file(self, url):
        """ Return a readable file-object object for the specified url. """

        protocol_name, address = url.split('://')
        print protocol_name, address
        
        protocol = self.resource_protocols[protocol_name]

        return protocol.file(address)

#### EOF ######################################################################
