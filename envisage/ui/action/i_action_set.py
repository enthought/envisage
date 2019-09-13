# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The action set interface. """


# Enthought library imports.
from traits.api import Dict, Interface, List, Str

# Local imports.
from .action import Action
from .group import Group
from .menu import Menu
from .tool_bar import ToolBar


class IActionSet(Interface):
    """ The action set interface.

    An action set is a collection of menus, groups, and actions.

    """

    # The action set's globally unique identifier.
    id = Str

    # The action set's name.
    #
    # fixme: This is not currently used, but in future it will be the name that
    # is shown to the user when they are customizing perspectives by adding or
    # removing action sets etc.
    name = Str

    # The actions in this set.
    actions = List(Action)

    # The groups in this set.
    groups = List(Group)

    # The menus in this set.
    menus = List(Menu)

    # The tool bars in this set.
    tool_bars = List(ToolBar)

    # A mapping from human-readable names to globally unique IDs.
    #
    # This mapping is used when interpreting the first item in a location path
    # (i.e., the **path** trait of a **Location** instance).
    #
    # When the path is intepreted, the first component (i.e., the first item
    # before any '/') is checked to see if it is in the mapping, and if so it
    # is replaced with the value in the map.
    #
    # This technique allows paths to start with human readable names, as
    # opposed to IDs (which are required in order to manage the namespace of
    # all action sets).
    #
    # For example, in the Envisage workbench, the menu bar ID is:
    #
    # ``'envisage.workbench.menubar'``
    #
    # Without aliases, you must specify a location like this:
    #
    # ``Location(path='envisage.workbench.menubar/ASubMenu/AGroup')``
    #
    # This is a bit long-winded! Instead, you can define an alias:
    #
    #     ``aliases = { 'MenuBar' : 'envisage.workbench.menubar' }``
    #
    # In that case, you can specify a location like this:
    #
    #     ``Location(path='MenuBar/ASubMenu/AGroup')``
    #
    aliases = Dict(Str, Str)

#### EOF ######################################################################
