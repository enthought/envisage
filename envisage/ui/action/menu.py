# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The *definition* of a menu in a menu bar or menu. """

# Enthought library imports.
from traits.api import Instance, List, Str

# Local imports.
from .group import Group
from .location import Location


class CGroup(Instance):
    """A trait type for a 'Group' or anything that can be cast to a 'Group'.

    Currently, the only cast allowed is from string -> Group using the
    string as the group's ID.

    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **kw):
        """Constructor."""

        super().__init__(klass=Group, **kw)

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def validate(self, object, name, value):
        """Validate a value."""

        if isinstance(value, str):
            value = Group(id=value)

        return super().validate(object, name, value)


class Menu(Location):
    """The *definition* of a menu in a menu bar or menu."""

    # The menu's unique identifier (unique within the group that the menu is to
    # be added to).
    id = Str

    # The menu name (appears on the menu bar or menu).
    name = Str

    # The groups in the menu.
    groups = List(CGroup)

    # The optional name of a class that implements the menu. The class must
    # support the **pyface.action.MenuManager** protocol.
    class_name = Str

    ###########################################################################
    # 'object' interface
    ###########################################################################

    def __str__(self):
        """Return the 'informal' string representation of the object."""

        return "Menu(%s)" % self.name

    __repr__ = __str__

    ###########################################################################
    # 'Menu' interface
    ###########################################################################

    def _id_default(self):
        """Trait initializer."""

        return self.name.strip("&")
