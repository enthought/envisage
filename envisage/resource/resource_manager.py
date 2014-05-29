""" The default resource manager. """


# Enthought library imports.
from traits.api import Dict, HasTraits, Str, provides

# Local imports.
from .i_resource_manager import IResourceManager
from .i_resource_protocol import IResourceProtocol


@provides(IResourceManager)
class ResourceManager(HasTraits):
    """ The default resource manager. """

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
        from .file_resource_protocol import FileResourceProtocol
        from .http_resource_protocol import HTTPResourceProtocol
        from .package_resource_protocol import PackageResourceProtocol

        resource_protocols = {
            'file'    : FileResourceProtocol(),
            'http'    : HTTPResourceProtocol(),
            'pkgfile' : PackageResourceProtocol()
        }

        return resource_protocols

    #### Methods ##############################################################

    def file(self, url):
        """ Return a readable file-like object for the specified url. """

        protocol_name, address = url.split('://')

        protocol = self.resource_protocols.get(protocol_name)
        if protocol is None:
            raise ValueError('unknown protocol in URL %s' % url)

        return protocol.file(address)

#### EOF ######################################################################
