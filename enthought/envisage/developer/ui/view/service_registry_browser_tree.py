""" The nodes used in the service registry browser tree. """


# Enthought library imports.
from enthought.envisage.api import IExtensionPoint, IServiceRegistry
from enthought.traits.api import Undefined
from enthought.traits.ui.api import TreeNode

# fixme: non-api imports.
from enthought.traits.ui.value_tree import SingleValueTreeNodeObject
from enthought.traits.ui.value_tree import value_tree_nodes


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
            node._protocol_ = protocol
            
            nodes.append(node)

        return nodes

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return IServiceRegistry(obj, Undefined) is obj


class IExtensionPointTreeNode(TreeNode):
    """ A tree node for an extension point. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        # fixme: This could be uglier, but I can't work out how ;^)
        index    = 0
        children = []
        for extension in obj.service_registry.get_extensions(obj.id):
            parent = ListNodeObject(parent=self, value=obj, _index=index)
            children.append(parent.node_for('', extension))
            index += 1
                            
        return children

    def get_label(self, obj):
        """ Get the object's label. """

        return obj.id
    
    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return IExtensionPoint(obj, Undefined) is obj

    # We override the following methods because 'ExtensionPoint' instances
    # are trait *types* and hence do not actually have traits themselves (i.e.
    # they do not inherit from 'HasTraits'). The default implementations of
    # these methods in 'TreeNode' attempt to call 'on_trait_change' to hook
    # up the listenrs, but obviously, if they don't have traits they don't have
    # 'on_trait_change' either ;^)
    #
    # fixme: If we make this node readonly will these go away?!?
    def when_label_changed(self, obj, callback, remove):
        """ Set up or remove listeners for label changes. """
        
        return

    def when_children_replaced(self, obj, callback, remove):
        """ Set up or remove listeners for children being replaced. """

        return

    def when_children_changed(self, obj, callback, remove):
        """ Set up or remove listenrs for children being changed. """
        
        return


service_registry_browser_tree_nodes = [
    IServiceRegistryTreeNode(
        auto_open = True,
        label     = '=Services',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),

    IExtensionPointTreeNode(
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),
] + value_tree_nodes

#### EOF ######################################################################
