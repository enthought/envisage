""" The nodes used in the service registry browser tree. """


# Enthought library imports.
from envisage.api import IExtensionPoint, IServiceRegistry
from traits.api import Any, Dict, HasTraits, Instance, Int, List
from traits.api import Property, Str, Undefined
from traitsui.api import TreeNode

# fixme: non-api imports.
from traitsui.value_tree import SingleValueTreeNodeObject
from traitsui.value_tree import value_tree_nodes



class ServiceModel(HasTraits):
    """ A model of a registered service. """

    # The service Id.
    id = Int

    # The service object.
    obj = Any

    # The service properties.
    properties = Dict


class ProtocolModel(HasTraits):
    """ A model of all of the services of a single protocol. """

    # The protocol (i.e. type) name.
    name = Str

    # All of the services offered for the protocol.
    services = List(ServiceModel)


class ServiceRegistryModel(HasTraits):
    """ A model of a service registry.

    This model groups services by protocol.

    """

    # The service registry that we are a model of.
    service_registry = Instance(IServiceRegistry)

    # The protocols contained in the registry.
    protocols = Property(List(ProtocolModel))

    ###########################################################################
    # 'ServiceRegistryModel' interface.
    ###########################################################################

    def _get_protocols(self):
        """ Trait property getter. """

        # fixme: Reaching into service registry. Not only is it ugly, but it
        # only works for the default implementation. Need to make this kind
        # of information available via the public API.
        all_services = list(self.service_registry._services.items())

        protocols = {}
        for service_id, (protocol_name, obj, properties) in all_services:
            protocol = protocols.get(protocol_name)
            if protocol is None:
                protocol = ProtocolModel(name=protocol_name)
                protocols[protocol_name] = protocol

            service_model = ServiceModel(
                id         = service_id,
                obj        = obj,
                properties = properties
            )

            protocol.services.append(service_model)

        return list(protocols.values())


class ProtocolModelTreeNode(TreeNode):
    """ A tree node for a protocol model. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        svtno = SingleValueTreeNodeObject()

        nodes = []
        for service in obj.services:
            node = svtno.node_for(repr(service.obj), service.obj)
            node._protocol_   = obj.name
            node._service_id_ = service.id
            nodes.append(node)

        return nodes


service_registry_browser_tree_nodes = [
    TreeNode(
        node_for  = [ServiceRegistryModel],
        auto_open = True,
        label     = '=Services',
        children  = 'protocols',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),

    ProtocolModelTreeNode(
        node_for  = [ProtocolModel],
        auto_open = True,
        label     = 'name',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),
] + value_tree_nodes

#### EOF ######################################################################
