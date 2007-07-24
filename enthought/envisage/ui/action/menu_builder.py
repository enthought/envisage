""" Builds menus from action, group, and menu extensions. """


# Enthought library imports.
from enthought.pyface.action.api import ActionManager, MenuBarManager
from enthought.pyface.action.api import MenuManager
from enthought.traits.api import Callable, HasTraits, Instance, List

# Local imports.
from action_set import ActionSet
from action_set_manager import ActionSetManager


class MenuBuilder(HasTraits):
    """ Builds menus from action, group, and menu extensions. """

    #### 'MenuBuilder' interface ##############################################

    # A factory that produces action implementations from definitions.
    action_factory = Callable

    # A factory that produces group implementations from definitions.
    group_factory = Callable

    # A factory that produces menu manager implementations from definitions.
    menu_factory = Callable

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

        # Add all groups and menus.
        self._add_groups_and_menus(menu_manager, self._action_set_manager,root)
        
        # Add all of the actions.
        self._add_actions(menu_manager, self._action_set_manager, root)

        return

    ###########################################################################
    # Protected 'MenuBuilder' interface.
    ###########################################################################

##     def _create_action(self, action_definition):
##         """ Creates an action implementation from an action definition. """

##         if self.action_factory is not None:
##             action = self.action_factory(action_definition)

##         else:
##             raise NotImplementedError

##         return action

##     def _create_group(self, group_definition):
##         """ Creates a group implementation from a group definition. """

##         if self.group_factory is not None:
##             group = self.group_factory(group_definition)

##         else:
##             raise NotImplementedError

##         return group

##     def _create_menu_manager(self, menu_definition):
##         """ Creates a menu manager implementation from a menu definition. """

##         if self.menu_factory is not None:
##             menu = self.menu_factory(menu_definition)
##             for group_definition in menu_definition.groups:
##                 menu.append(self._create_group(group_definition))

##         else:
##             raise NotImplementedError

##         return menu

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handler #################################################

    def _action_sets_changed(self, old, new):
        """ Static trait change handler. """

        self._action_set_manager.action_sets = new

        return
    
    #### Methods ##############################################################

    def _add_actions(self, menu_manager, action_set_manager, root):
        """ Adds all of the actions to the menu manager. """

        actions = action_set_manager.get_actions(root)

        while len(actions) > 0:
            start = len(actions)

            for action in actions[:]:
                # Resolve the path to find the menu manager that we are about
                # to add the action to.
                #
                # If any of the menu in path are missing then this creates them
                # (think 'mkdirs'!).
                target = self._make_submenus(menu_manager, action.path)

                # If a specific group is requested then make sure it exists.
                if len(action.group) > 0:
                    group = target.find_group(action.group)

                # Otherwise, just put the action in the last group on the menu.
                else:
                    group = target.find_group('additions')

                if group is None:
                    msg = 'No such group (%s) for %s' % (action.group, action)
                    raise ValueError(msg)

                elif self._add_action(action, group):
                    actions.remove(action)

            end = len(actions)

            # If we didn't succeed in placing *any* actions then we must have a
            # problem!
            if start == end:
                raise ValueError('Could not place %s' % actions)

        return

    def _add_action(self, action, group):
        """ Add an action to a group.

        Return True if the action was added successfully.

        Return False if the action needs to be placed 'before' or 'after' some
        other action, but the other action has not yet been added.

        """

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

    def _add_groups_and_menus(self, menu_manager, action_set_manager, root):
        """ Add the group and menu structure. """

        # Get all of the groups and menus.
        #
        # The reason we do the groups and menus together is that as we iterate
        # over the list, we might need to add a group before we can add a menu
        # and we might need to add a menu before we can add a group! Hence, we
        # take multiple passes over the list and we only barf if, in any single
        # iteration, we cannot place anything.
        groups_and_menus = action_set_manager.get_groups(root)
        groups_and_menus.extend(action_set_manager.get_menus(root))

        while len(groups_and_menus) > 0:
            start = len(groups_and_menus)

            for item in groups_and_menus[:]:
                path = item.path

                # Resolve the path to find the menu manager that we are about
                # to add the sub-menu or group to.
                target = self._find_menu_manager(menu_manager, path)
                if target is None:
                    continue
                    
                # Attempt to place a group.
                if self._is_group(item):
                    if self._add_group(target, item):
                        groups_and_menus.remove(item)

                # Attempt to place a menu.
                else:
                    if len(item.group) > 0:
                        group = target.find_group(item.group)
                        
                    else:
                        group = target.find_group('additions')

                    if group is None:
                        continue
                        
                    if self._add_menu(group, item):
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
            # it is always the last one!
            additions = menu_manager.find_group('additions')
            if additions is not None:
                index = menu_manager.groups.index(additions)

            else:
                index = len(menu_manager.groups)

        menu_manager.insert(index, self._create_group(group))

        return True

    def _add_menu(self, group, menu):
        """ Add a menu manager to a group.

        Return True if the menu was added successfully.

        Return False if the menu needs to be placed 'before' or 'after' some
        other item, but the other item has not yet been added.

        """

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

    def _is_group(self, item):
        """ Return True if item is a group *definition*, otherwise False. """

        return not hasattr(item, 'groups')

    def _make_submenus(self, menu_manager, path):
        """ Retutn the menu manager identified by the path.

        Make any intermediate menu-managers that are missing.

        """

        components = path.split('/')

        # We skip the first component, because if the path is of length 1, then
        # the target menu manager is the menu manager passed in (and 
        for component in components[1:]:
            item = menu_manager.find_item(component)
            if item is None:
                item = MenuManager(id=component, name=component)
                menu_manager.append(item)
                
            if not isinstance(item, ActionManager):
                raise '%s is not a menu in path %s' % (component, path)

            menu_manager = item

        return menu_manager
        
#### EOF ######################################################################
