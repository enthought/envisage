# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A menu builder that doesn't build real actions! """

from pyface.action.api import Action, Group, MenuBarManager, MenuManager

# Enthought library imports.
from envisage.ui.action.api import AbstractActionManagerBuilder


class DummyActionManagerBuilder(AbstractActionManagerBuilder):
    """An action manager builder that doesn't build real actions!

    This makes it very easy to test!

    """

    ###########################################################################
    # 'DummyActionManagerBuilder' interface.
    ###########################################################################

    def create_menu_bar_manager(self, root):
        """Create a menu bar manager from the builder's action sets."""

        menu_bar_manager = MenuBarManager(id="MenuBar")

        self.initialize_action_manager(menu_bar_manager, root)

        return menu_bar_manager

    ###########################################################################
    # Protected 'AbstractActionManagerBuilder' interface.
    ###########################################################################

    def _create_action(self, action_definition):
        """Create an action implementation from a definition."""

        return Action(name=action_definition.class_name)

    def _create_group(self, group_definition):
        """Create a group implementation from a definition."""

        return Group(id=group_definition.id)

    def _create_menu_manager(self, menu_definition):
        """Create a menu manager implementation from a definition."""

        menu_manager = MenuManager(id=menu_definition.id)
        for group_definition in menu_definition.groups:
            menu_manager.insert(-1, Group(id=group_definition.id))

        return menu_manager
