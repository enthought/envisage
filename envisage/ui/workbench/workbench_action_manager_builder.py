# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The action manager builder used to build the workbench menu/tool bars. """


# Standard library imports.
import weakref

from pyface.action.api import Action, Group, MenuManager
from pyface.workbench.action.api import MenuBarManager, ToolBarManager
from traits.api import Any, Instance

# Enthought library imports.
from envisage.ui.action.api import AbstractActionManagerBuilder


class WorkbenchActionManagerBuilder(AbstractActionManagerBuilder):
    """
    The action manager builder used to build the workbench menu/tool bars.
    """

    #### 'WorkbenchActionManagerBuilder' interface ############################

    # The workbench window that we build the menu and tool bars for.
    window = Instance("envisage.ui.workbench.api.WorkbenchWindow")

    #### Private interface ####################################################

    # All action implementations.
    _actions = Any

    ###########################################################################
    # Protected 'AbstractActionManagerBuilder' interface.
    ###########################################################################

    def _create_action(self, definition):
        """Create an action implementation from an action definition."""

        traits = {"window": self.window}

        # Override any traits that can be set in the definition.
        if len(definition.name) > 0:
            traits["name"] = definition.name

        if len(definition.class_name) > 0:
            action = self._actions.get(definition.class_name)
            if action is None:
                klass = self._import_symbol(definition.class_name)
                action = klass(**traits)
                self._actions[definition.class_name] = action

        # fixme: Do we ever actually do this? It seems that in Envisage 3.x
        # we always specify an action class!?!
        else:
            action = Action(**traits)

        # fixme: We need to associate the action set with the action to
        # allow for dynamic enabling/disabling etc. This is a *very* hacky
        # way to do it!
        action._action_set_ = definition._action_set_

        return action

    def _create_group(self, definition):
        """Create a group implementation from a group definition."""

        traits = {}

        # Override any traits that can be set in the definition.
        if len(definition.id) > 0:
            traits["id"] = definition.id

        if len(definition.class_name) > 0:
            klass = self._import_symbol(definition.class_name)

        else:
            klass = Group

        group = klass(**traits)

        # fixme: We need to associate the action set with the action to
        # allow for dynamic enabling/disabling etc. This is a *very* hacky
        # way to do it!
        group._action_set_ = definition._action_set_

        return group

    def _create_menu_manager(self, definition):
        """Create a menu manager implementation from a menu definition."""

        # fixme: 'window' is not actually a trait on 'MenuManager'! We set
        # it here to allow the 'View' menu to be created. However, it seems
        # that menus and actions etc should *always* have a reference to
        # the window that they are in?!?
        traits = {"window": self.window}

        # Override any traits that can be set in the definition.
        if len(definition.id) > 0:
            traits["id"] = definition.id

        if len(definition.name) > 0:
            traits["name"] = definition.name

        if len(definition.class_name) > 0:
            klass = self._import_symbol(definition.class_name)

        else:
            klass = MenuManager

        menu_manager = klass(**traits)

        # Add any groups to the menu.
        for group in definition.groups:
            group._action_set_ = definition._action_set_
            menu_manager.insert(-1, self._create_group(group))

        # fixme: We need to associate the action set with the action to
        # allow for dynamic enabling/disabling etc. This is a *very* hacky
        # way to do it!
        menu_manager._action_set_ = definition._action_set_

        return menu_manager

    def _create_menu_bar_manager(self):
        """Create a menu bar manager from the builder's action sets."""

        return MenuBarManager(window=self.window)

    def _create_tool_bar_manager(self, definition):
        """Create a tool bar manager implementation from a definition."""

        traits = {"window": self.window, "show_tool_names": False}

        # Override any traits that can be set in the definition.
        if len(definition.id) > 0:
            traits["id"] = definition.id

        if len(definition.name) > 0:
            traits["name"] = definition.name

        if len(definition.class_name) > 0:
            klass = self._import_symbol(definition.class_name)
        else:
            klass = ToolBarManager

        # fixme: 'window' is not actually a trait on 'ToolBarManager'! We
        # set it here because it is set on the 'MenuManager'! However, it
        # seems that menus and actions etc should *always* have a reference
        # to the window that they are in?!?
        tool_bar_manager = klass(**traits)

        # Add any groups to the tool bar.
        for group in definition.groups:
            group._action_set_ = definition._action_set_
            tool_bar_manager.insert(-1, self._create_group(group))

        # fixme: We need to associate the action set with the action to
        # allow for dynamic enabling/disabling etc. This is a *very* hacky
        # way to do it!
        tool_bar_manager._action_set_ = definition._action_set_

        return tool_bar_manager

    ###########################################################################
    # Private interface.
    ###########################################################################

    def __actions_default(self):
        """Trait initializer."""

        return weakref.WeakValueDictionary()

    def _import_symbol(self, symbol_path):
        """Import a symbol."""

        return self.window.application.import_symbol(symbol_path)
