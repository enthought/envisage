""" The tree editor used in the application browser. """


# Enthought library imports.
from enthought.envisage.api import IApplication, IPlugin
from enthought.traits.api import Undefined
from enthought.traits.ui.api import TreeEditor, TreeNode


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

        return False

    def is_node_for(self, obj):
        """ Returns whether this is the node that handles a specified object.
        
        """

        return IPlugin(obj, Undefined) is obj


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

    IPluginTreeNode(
        label     = 'name',
        rename    = False,
        copy      = False,
        delete    = False,
        insert    = False,
        menu      = None,
    )
]


application_browser_tree_editor = TreeEditor(
    nodes       = application_browser_tree_nodes,
    editable    = False,
    orientation = 'vertical',
    hide_root   = False,
    show_icons  = True,
    selected    = 'selection',
    on_dclick   = 'object.dclick'
)

#### EOF ######################################################################
