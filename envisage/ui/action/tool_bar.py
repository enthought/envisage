""" The *definition* of a tool bar. """

import sys

# Enthought library imports.
from traits.api import Instance, List, Str

# Local imports.
from .group import Group
from .location import Location

STRING_BASE_CLASS = basestring if sys.version_info[0] <= 2 else str

# fixme: Remove duplication (in menu.py too!)
class CGroup(Instance):
    """ A trait type for a 'Group' or anything that can be cast to a 'Group'.

    Currently, the only cast allowed is from string -> Group using the
    string as the group's ID.

    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **kw):
        """ Constructor. """

        super(CGroup, self).__init__(klass=Group, **kw)

        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def validate(self, object, name, value):
        """ Validate a value. """

        if isinstance(value, STRING_BASE_CLASS):
            value = Group(id=value)

        return super(CGroup, self).validate(object, name, value)


class ToolBar(Location):
    """ The *definition* of a menu in a menu bar or menu. """

    # The tool bars's unique identifier (unique within the multi-toolbar
    # that the tool bar is to be added to).
    id = Str

    # The tool bar name (appears when the tool bar is 'undocked').
    name = Str

    # The groups in the tool bar.
    groups = List(CGroup)

    # The optional name of a class that implements the tool bar. The class must
    # support the **pyface.action.ToolBarManager** protocol.
    class_name = Str

    ###########################################################################
    # 'object' interface
    ###########################################################################

    def __str__(self):
        """ Return the 'informal' string representation of the object. """

        return 'ToolBar(%s)' % self.name

    __repr__ = __str__

    ###########################################################################
    # 'Location' interface
    ###########################################################################

    def _path_default(self):
        """ Trait initializer. """

        return 'ToolBar'

    ###########################################################################
    # 'ToolBar' interface
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        return self.name

#### EOF ######################################################################
