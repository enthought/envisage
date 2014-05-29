""" The interface for action manager builders. """


# Enthought library imports.
from traits.api import Interface, List

# Local imports.
from .action_set import ActionSet


class IActionManagerBuilder(Interface):
    """ The interface for action manager builders.

    An action manager builder populates action managers (i.e. menus, menu bars
    and tool bars) from the menus, groups and actions defined in its action
    sets.

    """

    # The action sets used by the builder.
    action_sets = List(ActionSet)

    def initialize_action_manager(self, action_manager, root):
        """ Initialize an action manager from the builder's action sets.

        """

#### EOF ######################################################################
