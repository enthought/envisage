""" Builds menus from action, group, and menu extensions. """


# Enthought library imports.
from enthought.pyface.action.api import Action, Group, MenuBarManager
from enthought.pyface.action.api import MenuManager
from enthought.traits.api import Any, HasTraits, List

# Local imports.
from action_set_manager import ActionSetManager

class MenuBuilder(HasTraits):
    """ Builds menus from action, group, and menu extensions. """

    #### 'MenuBuilder' interface ##############################################

    # A factory that produces action implementations from definitions.
    action_factory = Any

    # A factory that produces group implementations from definitions.
    group_factory = Any

    # A factory that produces menu manager implementations from definitions.
    menu_factory = Any

    # The action sets used in the menu builder.
    action_sets = List
    
    ###########################################################################
    # 'MenuBuilder' interface.
    ###########################################################################

    def create_menu_bar_manager(self, root):
        """ Create a menu bar manager from the builder's action sets. """

        action_set_manager = ActionSetManager(action_sets=self.action_sets)

        menu_bar_manager = MenuBarManager(id='MenuBar')
        self.initialize_menu_manager(menu_bar_manager,action_set_manager,root)

        return menu_bar_manager
        
    def initialize_menu_manager(self, menu_manager, action_set_manager, root):
        """ Initializes a menu manager from an action set manager. """

        # Add all menus and groups.
        self._add_menus_and_groups(menu_manager, action_set_manager, root)

        # Add all of the actions.
        self._add_actions(menu_manager, action_set_manager, root)

        return

    ###########################################################################
    # Protected 'MenuBuilder' interface.
    ###########################################################################

    def _create_action(self, action_extension):
        """ Creates an action implementation from an action extension. """

        if self.action_factory is not None:
            action = self.action_factory.create_action(action_extension)

        else:
            raise NotImplementedError

        return action

    def _create_group(self, group_extension):
        """ Creates a group implementation from a group extension. """


        if self.group_factory is not None:
            group = self.group_factory.create_group(group_extension)

        else:
            raise NotImplementedError

        return group

    def _create_menu_manager(self, menu_extension):
        """ Creates a menu manager implementation from a menu extension. """

        if self.menu_factory is not None:
            menu = self.menu_factory.create_menu(menu_extension)
            for group_extension in menu_extension.groups:
                menu.append(self._create_group(group_extension))

        else:
            raise NotImplementedError

        return menu

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_actions(self, menu_manager, action_set_manager, root):
        """ Adds all of the actions to the menu manager. """

        actions = action_set_manager.get_actions(root)

        while len(actions) > 0:
            start = len(actions)

            for action in actions[:]:
                path = action.location.path

                # Resolve the path to find the target menu manager (i.e. the
                # menu manager that we are about to add a sub-menu or group
                # to).
                target = self._find_menu_manager(menu_manager, path)
                if target is None:
                    raise ValueError('no such location %s' % path)
                
                if len(action.location.group) > 0:
                    group = target.find_group(action.location.group)
                    
                else:
                    group = target.find_group('additions')

                if group is not None:
                    if self._add_action(action, group):
                        actions.remove(action)

            end = len(actions)

            # If we didn't succeed in placing *any* actions then we must have a
            # problem!
            if start == end:
                raise ValueError("Could not place %s" % actions)

        return

    def _add_action(self, action, group):
        """ Add an action to a group.

        Return True if the action was added successfully.

        Return False if the action needs to be placed 'before' or 'after' some
        other action, but the other action has not yet been added to the group.

        """

        if len(action.location.before) > 0:
            item = group.find(action.location.before)
            if item is None:
                return False

            index = group.items.index(item)

        elif len(action.location.after) > 0:
            item = group.find(action.location.after)
            if item is None:
                return False

            index = group.items.index(item) + 1

        else:
            index = len(group.items)

        group.insert(index, self._create_action(action))

        return True

    def _add_menus_and_groups(self, menu_manager, action_set_manager, root):
        """ Add the menu and group structure. """

        # Get all of the menus and groups.
        menus_and_groups = action_set_manager.get_menus(root)
        menus_and_groups.extend(action_set_manager.get_groups(root))

        # Sort them by the number of components in their path (ie. put peers
        # next to each other). This reduces the number of times we have to
        # iterate to place items, and also makes error reporting easier.
        self._sort_by_path_len(menus_and_groups)
        
        while len(menus_and_groups) > 0:
            start = len(menus_and_groups)

            for item in menus_and_groups[:]:
                path = item.location.path

                # Resolve the path to find the target menu manager (i.e. the
                # menu manager that we are about to add a sub-menu or group
                # to).
                target = self._find_menu_manager(menu_manager, path)
                if target is None:
                    raise ValueError('no such location %s' % path)
                    
                # Attempt to place a group.
                if self._is_group(item):
                    if self._add_group(target, item):
                        menus_and_groups.remove(item)

                # Attempt to place a menu.
                else:
                    if len(item.location.group) > 0:
                        group = target.find_group(item.location.group)

                    else:
                        group = target.find_group('additions')

                    if group is not None and self._add_menu(group, item):
                        menus_and_groups.remove(item)
                            
            end = len(menus_and_groups)

            # If we didn't succeed in placing *any* menus or groups then we
            # must have a problem!
            if start == end:
                raise ValueError('Could not place %s' % menus_and_groups)

        return

    def _add_group(self, menu_manager, group):
        """ Adds a group to a menu manager.

        Returns **True** only if the group could be added.

        """

        if len(group.location.before) > 0:
            item = menu_manager.find_group(group.location.before)
            if item is None:
                return False

            index = menu_manager.groups.index(item)

        elif len(group.location.after) > 0:
            item = menu_manager.find_group(group.location.after)
            if item is None:
                return False

            index = menu_manager.groups.index(item) + 1

        else:
            index = len(menu_manager.groups)

        menu_manager.insert(index, self._create_group(group))

        return True

    def _add_menu(self, group, menu):
        """ Adds a menu manager to a group.

        Returns **True** only if the menu could be added.

        """

        if len(menu.location.before) > 0:
            item = group.find(menu.location.before)
            if item is None:
                return False

            index = group.items.index(item)

        elif len(menu.location.after) > 0:
            item = group.find(menu.location.after)
            if item is None:
                return False

            index = group.items.index(item) + 1

        else:
            index = len(group.items)

        group.insert(index, self._create_menu_manager(menu))

        return True

    def _find_menu_manager(self, menu_manager, path):
        """ Returns the menu manager at the specified path.

        Returns **None** if the menu manager cannot be found.

        """

        components = path.split('/')
        if len(components) == 1:
            menu_manager = menu_manager

        else:
            menu_manager = menu_manager.find_item('/'.join(components[1:]))

        return menu_manager

    def _is_group(self, item):
        """ Return True if item is a group *definition*, otherwise False. """

        return not hasattr(item, 'groups')

    def _sort_by_path_len(self, menus_and_groups):
        """ Sort the menus & groups by the number of components in their path.

        """

        def by_path_len(x, y):
            """ Compare items by the number of components in their path. """
            
            len_x = len(x.location.path.split('/'))
            len_y = len(y.location.path.split('/'))

            return cmp(len_x, len_y)

        menus_and_groups.sort(by_path_len)

        return

#### EOF ######################################################################
