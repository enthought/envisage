# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The location of a group, menu, or action, within an action hierarchy. """


# Enthought library imports.
from traits.api import HasTraits, Str


class Location(HasTraits):
    """The location of a group, menu, or action, within an action hierarchy."""

    # A forward-slash-separated path through the action hierarchy to the menu
    # to add the action, group or menu to.
    #
    # Examples
    # --------
    #
    # * To add an item to the menu bar: ``path = "MenuBar"``
    #
    # * To add an item to the tool bar: ``path = "ToolBar"``
    #
    # * To add an item to a sub-menu: ``path = "MenuBar/File/New"``
    #
    path = Str

    #### Placement of the action within the menu specified by the path ########

    # The ID of the group to add the action or menu to (you can't have nested
    # groups).
    group = Str

    # The item appears after the item with this ID.
    #
    # - for groups, this is the ID of another group.
    # - for menus and actions, this is the ID of another menu or action.
    after = Str

    # The action appears before the item with this ID.
    #
    # - for groups, this is the ID of another group.
    # - for menus and actions, this is the ID of another menu or action.
    before = Str
