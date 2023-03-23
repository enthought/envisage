# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Manages a collection of action sets. """


# Enthought library imports.
from traits.api import HasTraits, List

# Local imports.
from .action_set import ActionSet


class ActionSetManager(HasTraits):
    """Manages a collection of action sets."""

    #### 'ActionSetManager' interface #########################################

    # The action sets that this manager manages.
    action_sets = List(ActionSet)

    ###########################################################################
    # 'ActionSetManager' interface.
    ###########################################################################

    def get_actions(self, root):
        """Return all action definitions for a root."""

        return self._get_items(self.action_sets, "actions", root)

    def get_groups(self, root):
        """Return all group definitions for a root."""

        return self._get_items(self.action_sets, "groups", root)

    def get_menus(self, root):
        """Return all menu definitions for a root."""

        return self._get_items(self.action_sets, "menus", root)

    def get_tool_bars(self, root):
        """Return all tool bar definitions for a root."""

        return self._get_items(self.action_sets, "tool_bars", root)

    ###########################################################################
    # 'Private' interface.
    ###########################################################################

    def _get_items(self, action_sets, attribute_name, root):
        """Return all actions, groups or menus for a particular root.

        e.g. To get all of the groups::

            self._get_items(action_sets, 'groups', root)

        """

        items = []
        for action_set in action_sets:
            for item in getattr(action_set, attribute_name):
                if self._get_root(item.path, action_set.aliases) == root:
                    items.append(item)

                    # fixme: Hacky, but the model needs to maintain the
                    # action set that contributed the item.
                    item._action_set_ = action_set

                    # fixme: Even hackier if this is a menu then we need to
                    # tag the action set onto all of the groups.
                    if attribute_name in ["menus", "toolbars"]:
                        for group in item.groups:
                            group._action_set_ = action_set

        return items

    def _get_root(self, path, aliases):
        """Return the effective root for a path.

        If the first component of the path matches an alias, then we return
        the value of the alias.

        e.g. If the aliases are::

            {'MenuBar' : 'envisage.ui.workbench.menubar'}

        and the path is::

           'MenuBar/File/New'

        Then the effective root is::

            'envisage.ui.workbench.menubar'

        If the first component of the path does *not* match an alias, then it
        is returned as is.

        e.g. If the aliases are::

            {'ToolBar' : 'envisage.ui.workbench.toolbar'}

        and the path is::

           'MenuBar/File/New'

        Then the effective root is::

            'MenuBar'

        """

        components = path.split("/")
        if components[0] in aliases:
            root = aliases[components[0]]

        else:
            root = components[0]

        return root
