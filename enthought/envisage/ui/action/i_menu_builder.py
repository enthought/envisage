""" The interface for menu builders. """


# Enthought library imports.
from enthought.traits.api import Interface, List

# Local imports.
from action_set import ActionSet


class IMenuBuilder(Interface):
    """ The interface for menu builders.

    Menu builders builds menus from action, group, and menu extensions.

    """

    # The action sets used in the menu builder.
    action_sets = List(ActionSet)

    def create_menu_bar_manager(self, root):
        """ Create a menu bar manager from the builder's action sets.

        """
        
    def initialize_menu_manager(self, menu_manager, root):
        """ Initialize a menu manager.

        """

#### EOF ######################################################################
