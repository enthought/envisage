""" The tree editor used in the application browser. """


# Enthought library imports.
from envisage.api import IApplication, IExtensionPoint, IPlugin
from traits.api import Any, HasTraits, List, Str, Undefined
from traitsui.api import TreeEditor, TreeNode

# fixme: non-api imports.
from traitsui.value_tree import value_tree_nodes


class Container(HasTraits):
    """ A container. """

    # The object that contains the container ;^)
    parent = Any

    # The contents of the container.
    contents = List

    # The label.
    label = Str


class IApplicationTreeNode(TreeNode):
    """ A tree node for an Envisage application. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        return [plugin for plugin in obj]

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.

        """

        return IApplication(obj, Undefined) is obj


class IPluginTreeNode(TreeNode):
    """ A tree node for a Envisage plugins. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return False#True

    def get_children(self, obj):
        """ Get the object's children. """

        extension_points = Container(
            label    = 'Extension Points',
            parent   = obj,
            contents = obj.get_extension_points()
        )

        extensions   = Container(
            label    = 'Extensions',
            parent   = obj,
            contents = self._get_extensions(obj)
        )

        return [extension_points, extensions]

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.

        """

        return IPlugin(obj, Undefined) is obj



    def _get_extensions(self, plugin):

        from traitsui.value_tree import ListNode, StringNode

        class MyListNode(ListNode):
            label = Str
            def format_value(self, value):
                return self.label

        extensions = []
        for trait_name, trait in plugin.traits().items():
            if trait.extension_point is not None:
                node = MyListNode(label=trait.extension_point, value=plugin.get_extensions(trait.extension_point))

                extensions.append(node)

        return extensions

class IExtensionPointTreeNode(TreeNode):
    """ A tree node for an extension point. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return False

    def get_children(self, obj):
        """ Get the object's children. """

        return []

    def get_label(self, obj):
        """ Get the object's label. """

        return obj.id

    def when_label_changed(self, obj, callback, remove):
        return

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.

        """

        return IExtensionPoint(obj, Undefined) is obj


class ContainerTreeNode(TreeNode):
    """ A tree node for a Envisage plugins. """

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def allows_children(self, obj):
        """ Return True if this object allows children. """

        return True

    def get_children(self, obj):
        """ Get the object's children. """

        return obj.contents

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.

        """

        return isinstance(obj, Container)



application_browser_tree_nodes  = [
    IApplicationTreeNode(
        auto_open = True,
        label     = 'id',
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

    IPluginTreeNode(
        label     = 'name',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),

    ContainerTreeNode(
        label     = 'label',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    ),
] + value_tree_nodes

#### EOF ######################################################################
