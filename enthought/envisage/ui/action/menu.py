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

    ###########################################################################
    # 'object' interface
    ###########################################################################
    
    def __str__(self):
        """ Return the 'informal' string representation of the object. """

        return 'Menu(%s)' % self.id

    __repr__ = __str__

    ###########################################################################
    # 'Menu' interface
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """
        
        return self.name.strip('&')
        
#### EOF ######################################################################
