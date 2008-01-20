""" A view showing a summary of the running application. """


# Enthought library imports.
from enthought.envisage.api import IApplication, IPlugin
from enthought.traits.api import Any, HasTraits, Instance, Undefined
from enthought.traits.ui.api import Item, TreeEditor, TreeNode, View



class PluginBrowser(HasTraits):
    """ A model useful for browsing a plugin. """

    



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

    def get_children(self, obj):
        """ Get the object's children. """

        return []#plugin for plugin in obj]

    def dclick(self, obj):
        """ Handle an object being double-clicked. """

        print 'Double click', obj


        
## from enthought.traits.ui.value_tree import ValueTree, value_tree_nodes
## application_view = View(
##     Item(
##         name       = 'value',
##         show_label = False,

##         editor     = TreeEditor(
##             nodes       = value_tree_nodes,
##             editable    = False,
##             orientation = 'vertical',
##             hide_root   = False,
##             show_icons  = True
##         )
##     ),

##     resizable = True,
##     style     = 'custom',
##     title     = 'Application',

##     width     = .2,
##     height    = .4
## )


application_view = View(
    Item(
        name       = 'application',
        show_label = False,

        editor     = TreeEditor(
            nodes  = [
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
            ],

            editable    = False,
            orientation = 'vertical',
            hide_root   = False,
            show_icons  = True,
            selected    = 'selection',
        )
    ),

    resizable = True,
    style     = 'custom',
    title     = 'Application',

    width     = .2,
    height    = .4
)


class ApplicationBrowser(HasTraits):
    """ An application browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    # The application that we are browsing.
    application = Instance(IApplication)
    
    # The default traits UI view.
    traits_ui_view = application_view

    selection = Any


    def _selection_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        print 'Selection changed', trait_name, old, new

        return
    
#### EOF ######################################################################
