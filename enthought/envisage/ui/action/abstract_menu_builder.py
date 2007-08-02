""" Builds menus from action, group, and menu extensions. """


# Enthought library imports.
from enthought.pyface.action.api import ActionManager, MenuBarManager
from enthought.pyface.action.api import MenuManager
from enthought.traits.api import HasTraits, Instance, List

# Local imports.
from action_set import ActionSet
from action_set_manager import ActionSetManager
from group import Group


class AbstractMenuBuilder(HasTraits):
    """ Builds menus from action, group, and menu extensions.

    This class *must* be subclassed, and the following methods implemented::

      _create_action
      _create_group
      _create_menu_manager

    """

    #### 'MenuBuilder' interface ##############################################

    # The action sets used in the menu builder.
    action_sets = List(ActionSet)

    #### Private interface ####################################################

    _action_set_manager = Instance(ActionSetManager, ())
    
    ###########################################################################
    # 'MenuBuilder' interface.
    ###########################################################################

    def create_menu_bar_manager(self, root):
        """ Create a menu bar manager from the builder's action sets. """

        menu_bar_manager = MenuBarManager(id='MenuBar')

        self.initialize_menu_manager(menu_bar_manager, root)

        return menu_bar_manager
        
    def initialize_menu_manager(self, menu_manager, root):
        """ Initialize a menu manager. """

        # Get all of the groups and menus for the specified root.
        groups_and_menus = self._action_set_manager.get_groups(root)
        groups_and_menus.extend(self._action_set_manager.get_menus(root))

        # Add all groups and menus.
        self._add_groups_and_menus(menu_manager, groups_and_menus)

        # Get all actions for the specified root.
        actions = self._action_set_manager.get_actions(root)
        
        # Add all of the actions ot the menu manager.
        self._add_actions(menu_manager, actions)

        return

    ###########################################################################
    # Protected 'MenuBuilder' interface.
    ###########################################################################

    def _create_action(self, action_definition):
        """ Creates an action implementation from a definition. """

        raise NotImplementedError

    def _create_group(self, group_definition):
        """ Creates a group implementation from a definition. """

        raise NotImplementedError

    def _create_menu_manager(self, menu_manager_definition):
        """ Creates a menu manager implementation from a definition. """

        raise NotImplementedError

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handler #################################################

    def _action_sets_changed(self, old, new):
        """ Static trait change handler. """

        self._action_set_manager.action_sets = new

        return
    
    #### Methods ##############################################################

    def _add_actions(self, menu_manager, actions):
        """ Add the specified actions to the menu manager. """

        while len(actions) > 0:
            start = len(actions)

            for action in actions[:]:
                # Resolve the action's path to find the menu manager that it
                # should be added to.
                #
                # If any of the menus in path are missing then this creates
                # them automatically (think 'mkdirs'!).
                target = self._make_submenus(menu_manager, action.path)

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
                raise ValueError('Could not place %s' % actions)

        return

    def _add_action(self, menu_manager, action):
        """ Add an action to a menu manager.

        Return True if the action was added successfully.

        Return False if the action needs to be placed 'before' or 'after' some
        other action, but the other action has not yet been added.

        """

        group = self._find_group(menu_manager, action.group)
        if group is None:
            msg = 'No such group (%s) for %s' % (action.group, action)
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

    def _add_groups_and_menus(self, menu_manager, groups_and_menus):
        """ Add the specified groups and menus to the menu manager. """

        # The reason we put the groups and menus together is that as we iterate
        # over the list trying to add them, we might need to add a group before
        # we can add a menu and we might need to add a menu before we can add a
        # group! Hence, we take multiple passes over the list and we only barf
        # if, in any single iteration, we cannot place anything.
        while len(groups_and_menus) > 0:
            start = len(groups_and_menus)
            
            for item in groups_and_menus[:]:
                # Resolve the path to find the menu manager that we are about
                # to add the sub-menu or group to.
                target = self._find_menu_manager(menu_manager, item.path)
                if target is not None:
                    # Attempt to place a group.
                    if isinstance(item, Group):
                        if self._add_group(target, item):
                            groups_and_menus.remove(item)

                    # Attempt to place a menu.
                    elif self._add_menu(target, item):
                        groups_and_menus.remove(item)
                    
            end = len(groups_and_menus)
            
            # If we didn't succeed in placing *any* menus or groups then we
            # must have a problem!
            if start == end:
                raise ValueError('Could not place %s' % groups_and_menus)
        
        return

    def _add_group(self, menu_manager, group):
        """ Add a group to a menu manager.

        Return True if the group was added successfully.

        Return False if the group needs to be placed 'before' or 'after' some
        other group, but the other group has not yet been added.

        """

        if len(group.before) > 0:
            item = menu_manager.find_group(group.before)
            if item is None:
                return False

            index = menu_manager.groups.index(item)

        elif len(group.after) > 0:
            item = menu_manager.find_group(group.after)
            if item is None:
                return False

            index = menu_manager.groups.index(item) + 1

        else:
            # If the menu manger has an 'additions' group then make sure that
            # it is always the last one! In Pyface, the 'additions' groups is
            # created by default, so unless someone has explicitly removed it,
            # it *will* be there! 
            additions = menu_manager.find_group('additions')
            if additions is not None:
                index = menu_manager.groups.index(additions)

            else:
                index = len(menu_manager.groups)

        menu_manager.insert(index, self._create_group(group))

        return True

    def _add_menu(self, menu_manager, menu):
        """ Add a menu manager to a errr, menu manager.

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

        group.insert(index, self._create_menu_manager(menu))

        return True

    def _find_group(self, menu_manager, id):
        """ Find the group with the specified ID. """
        
        if len(id) > 0:
            group = menu_manager.find_group(id)

        else:
            group = menu_manager.find_group('additions')

        return group
    
    def _find_menu_manager(self, menu_manager, path):
        """ Return the menu manager at the specified path.

        Returns None if the menu manager cannot be found.

        """

        components = path.split('/')
        if len(components) == 1:
            menu_manager = menu_manager

        else:
            menu_manager = menu_manager.find_item('/'.join(components[1:]))

        return menu_manager

    def _make_submenus(self, menu_manager, path):
        """ Retutn the menu manager identified by the path.

        Make any intermediate menu-managers that are missing.

        """

        components = path.split('/')

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
                msg = '%s is not a menu in path %s' % (item, path)
                raise ValueError(msg)

            menu_manager = item

        return menu_manager
        
#### EOF ######################################################################
