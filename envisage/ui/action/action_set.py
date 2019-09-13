# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An action set is a collection of menus, groups, and actions. """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import Bool, Dict, HasTraits, List, Str, provides
from traits.util.camel_case import camel_case_to_words

# Local imports.
from .action import Action
from .group import Group
from .menu import Menu
from .tool_bar import ToolBar
from .i_action_set import IActionSet


# Logging.
logger = logging.getLogger(__name__)


@provides(IActionSet)
class ActionSet(HasTraits):
    """ An action set is a collection of menus, groups, and actions. """

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

    # Are the actions and menus in this set enabled (if they are disabled they
    # will be greyed out). Tool bars are generally not greyed out themselves,
    # but the actions within them are.
    enabled = Bool(True)

    # Are the actions, menus and tool bars in this set visible?
    visible = Bool(True)

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

    #### Trait initializers ###################################################

    def _id_default(self):
        """ Trait initializer. """

        id = '%s.%s' % (type(self).__module__, type(self).__name__)
        logger.warning('action set %s has no Id - using <%s>' % (self, id))

        return id

    def _name_default(self):
        """ Trait initializer. """

        name = camel_case_to_words(type(self).__name__)
        logger.warning('action set %s has no name - using <%s>' % (self, name))

        return name

#### EOF ######################################################################
