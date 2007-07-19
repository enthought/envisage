""" Manages contributions of action sets. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import HasTraits, List

# Local imports.
from action_set import ActionSet
from location import Location


# Logging.
logger = logging.getLogger(__name__)


class ActionSetManager(HasTraits):
    """ Manages contributions of action sets. """

    #### 'ActionSetManager' interface #########################################

    # The action sets that this manager manages.
    action_sets = List(ActionSet)

    ###########################################################################
    # 'ActionSetManager' interface.
    ###########################################################################

    # fixme: In all of these methods we should organize and cache the
    # contributions!
    def get_action(self, id, root):
        """ Return the action with the specified ID for a root.

        Return None if no such action exists.

        """

        actions = self.get_actions(root)
        for action in actions:
            if action.id == id:
                result = action
                break
        else:
            result = None

        return result

    def get_actions(self, root):
        """ Return all action contributions for a root. """

        logger.debug('%s retrieving actions for %s', self, root)

        actions = []
        for action_set in self.action_sets:
            aliases = action_set.aliases
            for action in action_set.actions:

                for i in range(len(action.locations)):
                    if not isinstance(action.locations[i], Location):
                        action.locations[i] = Location(path=action.locations[i])
                        
                    
                for location in action.locations:
                    if self._get_location_root(location, aliases) == root:
                        action._action_set_ = action_set
                        actions.append(action)
                        break

        return actions

    def get_groups(self, root):
        """ Returns all group contributions for a root. """

        groups = []
        for action_set in self.action_sets:
            aliases = action_set.aliases
            for group in action_set.groups:
                if self._get_location_root(group.location, aliases) == root:
                    group._action_set_ = action_set
                    groups.append(group)

        return groups

    def get_menus(self, root):
        """ Returns all menu contributions for a root. """

        menus = []
        for action_set in self.action_sets:
            aliases = action_set.aliases
            for menu in action_set.menus:
                from location import Location
                if not isinstance(menu.location, Location):
                    menu.location = Location(path=menu.location)
            
                
                if self._get_location_root(menu.location, aliases) == root:
                    menu._action_set_ = action_set
                    menus.append(menu)

        return menus

    ###########################################################################
    # 'Private' interface.
    ###########################################################################

    def _get_location_root(self, location, aliases):
        """ Returns the effective root for a location. """

        components = location.path.split('/')
        if components[0] in aliases:
            location_root = aliases[components[0]]

        else:
            location_root = components[0]

        return location_root

#### EOF ######################################################################
