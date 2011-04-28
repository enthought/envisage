""" The nodes used in the extension registry browser tree. """


# Enthought library imports.
from envisage.api import IExtensionPoint, IExtensionRegistry
from traits.api import Undefined
from traitsui.api import TreeNode

# fixme: non-api imports.
from traitsui.value_tree import SingleValueTreeNodeObject
from traitsui.value_tree import value_tree_nodes


class IExtensionRegistryTreeNode(TreeNode):
    """ A tree node for an extension registry. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        extension_points = obj.get_extension_points()

        # Tag the extension registry onto the extension points.
        for extension_point in extension_points:
            extension_point.__extension_registry__ = obj

        return extension_points

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.

        """

        return IExtensionRegistry(obj, Undefined) is obj


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
        for extension in obj.__extension_registry__.get_extensions(obj.id):
            parent = SingleValueTreeNodeObject(value=obj, _index=index)
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


extension_registry_browser_tree_nodes = [
    IExtensionRegistryTreeNode(
        auto_open = True,
        label     = '=Extension Points',
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
