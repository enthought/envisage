""" The interface for action manager builders. """


# Enthought library imports.
from enthought.traits.api import Interface, List

# Local imports.
from action_set import ActionSet


class IActionManagerBuilder(Interface):
    """ The interface for action manager builders.

    An action manager builder builds menus, menu bars and tool bars from action
    sets.

    """

    # The action sets used by the builder.
    action_sets = List(ActionSet)

    def create_menu_bar_manager(self, root):
        """ Create a menu bar manager from the builder's action sets.

        """
        
    def initialize_action_manager(self, action_manager, root):
        """ Initialize an action manager from the builder's action sets.

        """

#### EOF ######################################################################
