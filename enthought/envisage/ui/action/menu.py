""" A menu in a menu bar or menu. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Instance, List, Str

# Local imports.
from group import Group
from location import Location


class Menu(HasTraits):
    """ A menu in a menu bar or menu. """

    # The menu's unique identifier (unique within the group that the menu is to
    # be added to).
    id = Str

    # The menu name (appears on the menu bar or menu).
    name = Str

    # The groups in the menu.
    groups = List(Group)

    # The location of the menu.
    location = Any#Instance(Location)

    # The optional name of a class that implements the group. The class must
    # support the **enthought.pyface.action.MenuManager** interface.
    class_name = Str

    def __str__(self):
        return 'Menu(%s)' % self.id

    __repr__ = __str__


    def _id_default(self):
        return self.name.strip('&')

        
#### EOF ######################################################################
