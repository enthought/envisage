""" Manages a collection of action sets. """


# Enthought library imports.
from enthought.traits.api import HasTraits, List

# Local imports.
from action_set import ActionSet


class ActionSetManager(HasTraits):
    """ Manages a collection of action sets. """

    #### 'ActionSetManager' interface #########################################

    # The action sets that this manager manages.
    action_sets = List(ActionSet)

    ###########################################################################
    # 'ActionSetManager' interface.
    ###########################################################################

    def get_actions(self, root):
        """ Return all action definitions for a root. """

        return self._get_items(self.action_sets, 'actions', root)

    def get_groups(self, root):
        """ Return all group definitions for a root. """

        return self._get_items(self.action_sets, 'groups', root)

    def get_menus(self, root):
        """ Return all menu definitions for a root. """

        return self._get_items(self.action_sets, 'menus', root)

    def get_tool_bars(self, root):
        """ Return all tool bar definitions for a root. """

        return self._get_items(self.action_sets, 'tool_bars', root)

    ###########################################################################
    # 'Private' interface.
    ###########################################################################

    def _get_items(self, action_sets, attribute_name, root):
        """ Return all actions, groups or menus for a particular root.

        e.g. To get all of the groups::

            self._get_items(action_sets, 'groups', root)

        """

        items = []
        for action_set in action_sets:
            for item in getattr(action_set, attribute_name):
                if self._get_root(item.path, action_set.aliases) == root:
                    items.append(item)

        return items

    def _get_root(self, path, aliases):
        """ Return the effective root for a path.

        If the first component of the path matches an alias, then we return
        the value of the alias.
        
        e.g. If the aliases are::

            {'MenuBar' : 'enthought.envisage.ui.workbench.menubar'}

        and the path is::

           'MenuBar/File/New'

        Then the effective root is::

            'enthought.envisage.ui.workbench.menubar'

        If the first component of the path does *not* match an alias, then it
        is returned as is.

        e.g. If the aliases are::

            {'ToolBar' : 'enthought.envisage.ui.workbench.toolbar'}

        and the path is::

           'MenuBar/File/New'

        Then the effective root is::

            'MenuBar'
        
        """

        components = path.split('/')
        if components[0] in aliases:
            root = aliases[components[0]]

        else:
            root = components[0]

        return root

#### EOF ######################################################################
