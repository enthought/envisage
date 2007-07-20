""" An action in a menu bar, menu, or tool bar. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Instance, Str

# Local imports.
from location import Location


class Action(Location):
    """ An action in a menu bar, menu, or tool bar. """

    #### Action implementation ################################################

    # The name of the class that implements the action.
    class_name = Str

    #### Placement ############################################################

    # The locations of the action. Unlike groups and menus, actions can appear
    # in multiple locations, e.g., on a menu *and* on the tool bar.
    #location = Any#Instance(Location)

    ###########################################################################
    # 'object' interface
    ###########################################################################
    
    def __str__(self):
        """ Return the 'informal' string representation of the object. """

        return 'Action(%s)' % self.class_name

    __repr__ = __str__

##     ###########################################################################
##     # Private interface
##     ###########################################################################

##     def _location_changed(self, old, new):
##         """ Static trait change hanler. """

##         if not isinstance(new, Location):
##             self.location = Location(path=new)

##         return
    
#### EOF ######################################################################
