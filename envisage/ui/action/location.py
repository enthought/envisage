""" The location of a group, menu, or action, within an action hierarchy. """


# Enthought library imports.
from traits.api import HasTraits, Str


class Location(HasTraits):
    """ The location of a group, menu, or action, within an action hierarchy.

    """

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

#### EOF ######################################################################
