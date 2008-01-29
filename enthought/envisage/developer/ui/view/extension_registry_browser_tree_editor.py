""" The tree editor used in the extension registry browser. """


# Enthought library imports.
from enthought.envisage.api import IApplication, IExtensionPoint
from enthought.envisage.api import IExtensionRegistry, IPlugin
from enthought.traits.api import Undefined
from enthought.traits.ui.api import TreeEditor, TreeNode


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

        return obj.get_extension_points()

    def is_node_for(self, obj):
        """ Return whether this is the node that handles a specified object.
        
        """

        return IApplication(obj, Undefined) is obj


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
    )
]


extension_registry_browser_tree_editor = TreeEditor(
    nodes       = extension_registry_browser_tree_nodes,
    editable    = False,
    orientation = 'vertical',
    hide_root   = True,
    show_icons  = True,
#    selected    = 'selection',
    on_dclick   = 'object.dclick'
)

#### EOF ######################################################################
