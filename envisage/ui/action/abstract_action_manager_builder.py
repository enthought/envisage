# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Builds menus, menu bars and tool bars from action sets. """


# Enthought library imports.
from pyface.action.api import ActionManager, MenuManager
from traits.api import HasTraits, Instance, List, observe, provides

# Local imports.
from .action_set import ActionSet
from .action_set_manager import ActionSetManager
from .group import Group
from .i_action_manager_builder import IActionManagerBuilder


@provides(IActionManagerBuilder)
class AbstractActionManagerBuilder(HasTraits):
    """Builds menus, menu bars and tool bars from action sets.

    This class *must* be subclassed, and the following methods implemented::

      _create_action
      _create_group
      _create_menu_manager

    """

    #### 'IActionManagerBuilder' interface ####################################

    # The action sets used by the builder.
    action_sets = List(ActionSet)

    #### Private interface ####################################################

    _action_set_manager = Instance(ActionSetManager, ())

    ###########################################################################
    # 'IActionManagerBuilder' interface.
    ###########################################################################

    def create_menu_bar_manager(self, root):
        """Create a menu bar manager from the builder's action sets."""

        menu_bar_manager = self._create_menu_bar_manager()

        self.initialize_action_manager(menu_bar_manager, root)

        return menu_bar_manager

    # fixme: V3 refactor loooong (and confusing) method!
    def create_tool_bar_managers(self, root):
        """Creates all tool bar managers from the builder's action sets."""

        ########################################
        # New style (i.e multi) tool bars.
        ########################################

        tool_bar_managers = []
        for tool_bar in self._action_set_manager.get_tool_bars(root):
            # Get all of the groups for the tool bar.
            groups = []
            for group in self._action_set_manager.get_groups(root):
                if group.path.startswith("%s/%s" % (root, tool_bar.name)):
                    group.path = "/".join(group.path.split("/")[1:])
                    groups.append(group)

            # Get all of the actions for the tool bar.
            actions = []
            for action in self._action_set_manager.get_actions(root):
                if action.path.startswith("%s/%s" % (root, tool_bar.name)):
                    action.path = "/".join(action.path.split("/")[1:])
                    actions.append(action)

            # We don't add the tool bar if it is empty!
            if len(groups) + len(actions) > 0:
                tool_bar_manager = self._create_tool_bar_manager(tool_bar)

                # Add all groups and menus.
                self._add_groups_and_menus(tool_bar_manager, groups)

                # Add all of the actions ot the menu manager.
                self._add_actions(tool_bar_manager, actions)

                # Include the tool bar!
                tool_bar_managers.append(tool_bar_manager)

        ######################################################################
        # Scoop up old groups and actions for the old style (single) tool bar.
        ######################################################################

        # Get all of the groups for the tool bar.
        groups = []
        for group in self._action_set_manager.get_groups(root):
            if group.path == root:
                groups.append(group)

        # Get all of the actions for the tool bar.
        actions = []
        for action in self._action_set_manager.get_actions(root):
            if action.path == root:
                actions.append(action)

        # We don't add the tool bar if it is empty!
        if len(groups) + len(actions) > 0:
            from .tool_bar import ToolBar

            tool_bar_manager = self._create_tool_bar_manager(
                ToolBar(name="Tool Bar", path=root, _action_set_=None)
            )

            # Add all groups and menus.
            self._add_groups_and_menus(tool_bar_manager, groups)

            # Add all of the actions ot the menu manager.
            self._add_actions(tool_bar_manager, actions)

            # Include the tool bar!
            tool_bar_managers.insert(0, tool_bar_manager)

        return tool_bar_managers

    def initialize_action_manager(self, action_manager, root):
        """Initialize an action manager from the builder's action sets."""

        # Get all of the groups and menus for the specified root (for toolbars
        # there will **only** be groups).
        groups_and_menus = self._action_set_manager.get_groups(root)
        groups_and_menus.extend(self._action_set_manager.get_menus(root))

        # Add all groups and menus.
        self._add_groups_and_menus(action_manager, groups_and_menus)

        # Get all actions for the specified root.
        actions = self._action_set_manager.get_actions(root)

        # Add all of the actions ot the menu manager.
        self._add_actions(action_manager, actions)

    ###########################################################################
    # Protected 'AbstractActionManagerBuilder' interface.
    ###########################################################################

    def _create_action(self, action_definition):
        """Creates an action implementation from a definition."""

        raise NotImplementedError

    def _create_group(self, group_definition):
        """Creates a group implementation from a definition."""

        raise NotImplementedError

    def _create_menu_manager(self, menu_manager_definition):
        """Creates a menu manager implementation from a definition."""

        raise NotImplementedError

    def _create_menu_bar_manager(self):
        """Creates a menu bar manager implementation."""

        raise NotImplementedError

    def _create_tool_bar_manager(self, tool_bar_definition):
        """Creates a tool bar manager implementation from a definition."""

        raise NotImplementedError

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handler #################################################

    @observe("action_sets")
    def _update_action_sets_on_manager(self, event):
        """Static trait change handler."""
        new = event.new
        self._action_set_manager.action_sets = new

    #### Methods ##############################################################

    def _add_actions(self, action_manager, actions):
        """Add the specified actions to an action manager."""

        while len(actions) > 0:
            start = len(actions)

            for action in actions[:]:
                # Resolve the action's path to find the action manager that it
                # should be added to.
                #
                # If any of the menus in path are missing then this creates
                # them automatically (think 'mkdirs'!).
                target = self._make_submenus(action_manager, action.path)

                # Attempt to place the action.
                #
                # If the action needs to be placed 'before' or 'after' some
                # other action, but the other action has not yet been added
                # then we will try again later!
                if self._add_action(target, action):
                    actions.remove(action)

            end = len(actions)

            # If we didn't succeed in placing *any* actions then we must have a
            # problem!
            if start == end:
                raise ValueError("Could not place %s" % actions)

    def _add_action(self, action_manager, action):
        """Add an action to an action manager.

        Return True if the action was added successfully.

        Return False if the action needs to be placed 'before' or 'after' some
        other action, but the other action has not yet been added.

        """

        group = self._find_group(action_manager, action.group)
        if group is None:
            msg = "No such group (%s) for %s" % (action.group, action)
            raise ValueError(msg)

        if len(action.before) > 0:
            item = group.find(action.before)
            if item is None:
                return False

            index = group.items.index(item)

        elif len(action.after) > 0:
            item = group.find(action.after)
            if item is None:
                return False

            index = group.items.index(item) + 1

        else:
            index = len(group.items)

        group.insert(index, self._create_action(action))

        return True

    def _add_groups_and_menus(self, action_manager, groups_and_menus):
        """Add the specified groups and menus to an action manager."""

        # The reason we put the groups and menus together is that as we iterate
        # over the list trying to add them, we might need to add a group before
        # we can add a menu and we might need to add a menu before we can add a
        # group! Hence, we take multiple passes over the list and we only barf
        # if, in any single iteration, we cannot add anything.
        while len(groups_and_menus) > 0:
            start = len(groups_and_menus)

            for item in groups_and_menus[:]:
                # Resolve the path to find the menu manager that we are about
                # to add the sub-menu or group to.
                target = self._find_action_manager(action_manager, item.path)
                if target is not None:
                    # Attempt to place a group.
                    if isinstance(item, Group):
                        if self._add_group(target, item):
                            groups_and_menus.remove(item)

                    # Attempt to place a menu.
                    elif self._add_menu(target, item):
                        groups_and_menus.remove(item)

            end = len(groups_and_menus)

            # If we didn't succeed in adding *any* menus or groups then we
            # must have a problem!
            if start == end:
                raise ValueError("Could not place %s" % groups_and_menus)

    def _add_group(self, action_manager, group):
        """Add a group to an action manager.

        Return True if the group was added successfully.

        Return False if the group needs to be placed 'before' or 'after' some
        other group, but the other group has not yet been added.

        """

        # Does the group already exist in the menu? If not then add it,
        # otherwise do nothing.
        if action_manager.find_group(group.id) is None:
            if len(group.before) > 0:
                item = action_manager.find_group(group.before)
                if item is None:
                    return False

                index = action_manager.groups.index(item)

            elif len(group.after) > 0:
                item = action_manager.find_group(group.after)
                if item is None:
                    return False

                index = action_manager.groups.index(item) + 1

            else:
                # If the menu manager has an 'additions' group then make sure
                # that it is always the last one! In Pyface, the 'additions'
                # groups is created by default, so unless someone has
                # explicitly removed it, it *will* be there!
                additions = action_manager.find_group("additions")
                if additions is not None:
                    index = action_manager.groups.index(additions)

                else:
                    index = len(action_manager.groups)

            action_manager.insert(index, self._create_group(group))

        return True

    def _add_menu(self, menu_manager, menu):
        """Add a menu manager to a errr, menu manager.

        Return True if the menu was added successfully.

        Return False if the menu needs to be placed 'before' or 'after' some
        other item, but the other item has not yet been added.

        """

        group = self._find_group(menu_manager, menu.group)
        if group is None:
            return False

        if len(menu.before) > 0:
            item = group.find(menu.before)
            if item is None:
                return False

            index = group.items.index(item)

        elif len(menu.after) > 0:
            item = group.find(menu.after)
            if item is None:
                return False

            index = group.items.index(item) + 1

        else:
            index = len(group.items)

        # If the menu does *not* already exist in the group then add it.
        menu_item = group.find(menu.id)
        if menu_item is None:
            group.insert(index, self._create_menu_manager(menu))

        # Otherwise, add all of the new menu's groups to the existing one.
        else:
            for group in menu.groups:
                self._add_group(menu_item, group)

        return True

    def _find_group(self, action_manager, id):
        """Find the group with the specified ID."""

        if len(id) > 0:
            group = action_manager.find_group(id)

        else:
            group = action_manager.find_group("additions")

        return group

    def _find_action_manager(self, action_manager, path):
        """Return the action manager at the specified path.

        Returns None if the action manager cannot be found.

        """

        components = path.split("/")
        if len(components) == 1:
            action_manager = action_manager

        else:
            action_manager = action_manager.find_item("/".join(components[1:]))

        return action_manager

    def _make_submenus(self, menu_manager, path):
        """Retutn the menu manager identified by the path.

        Make any intermediate menu-managers that are missing.

        """

        components = path.split("/")

        # We skip the first component, because if the path is of length 1, then
        # the target menu manager is the menu manager passed in.
        for component in components[1:]:
            item = menu_manager.find_item(component)

            # If the menu manager does *not* contain an item with this ID then
            # create a sub-menu automatically.
            if item is None:
                item = MenuManager(id=component, name=component)
                menu_manager.append(item)

            # If the menu manager *does* already contain an item with this ID
            # then make sure it is a menu and not an action!
            elif not isinstance(item, ActionManager):
                msg = "%s is not a menu in path %s" % (item, path)
                raise ValueError(msg)

            menu_manager = item

        return menu_manager
