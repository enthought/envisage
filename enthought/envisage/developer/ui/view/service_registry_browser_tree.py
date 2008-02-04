""" The nodes used in the service registry browser tree. """


# Enthought library imports.
from enthought.envisage.api import IExtensionPoint, IServiceRegistry
from enthought.traits.api import Any, Dict, HasTraits, Instance, Int, List
from enthought.traits.api import Property, Str, Undefined
from enthought.traits.ui.api import TreeNode

# fixme: non-api imports.
from enthought.traits.ui.value_tree import SingleValueTreeNodeObject
from enthought.traits.ui.value_tree import value_tree_nodes



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

    # All of the service in the protocol.
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

        # fixme: Reaching into service registry. This only works for the
        # default implementation.
        all_services = self.service_registry._services.items()
        
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
            
        return protocols.values()


class ServiceRegistryModelTreeNode(TreeNode):
    """ A tree node for an service registry model. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        model = ServiceRegistryModel(service_registry=obj)
        
        return model.protocols

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return IServiceRegistry(obj, Undefined) is obj


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

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return isinstance(obj, ProtocolModel)


class ServiceModelTreeNode(TreeNode):
    """ A tree node for a service model. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        return obj.services

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return isinstance(obj, ProtocolModel)

    
class IServiceRegistryTreeNode(TreeNode):
    """ A tree node for an extension registry. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """


        services_by_type = {}

        print obj._services
        
        for id, (protocol, obj, properties) in obj._services.items():
            services = services_by_type.setdefault(protocol, [])
            services.append((id, obj, properties))
            

        svtno = SingleValueTreeNodeObject()

        nodes = []
        for protocol, services in services_by_type.items():
            node = svtno.node_for(protocol, services)
            node._protocol_  = protocol
            
            nodes.append(node)

        return nodes

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return IServiceRegistry(obj, Undefined) is obj



service_registry_browser_tree_nodes = [
##     IServiceRegistryTreeNode(
##         auto_open = True,
##         label     = '=Services',
##         rename    = False,
##         copy      = False,
##         delete    = False,
##         insert    = False,
##         menu      = None,
##     ),

    ServiceRegistryModelTreeNode(
        auto_open = True,
        label     = '=Services',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),

    ProtocolModelTreeNode(
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
