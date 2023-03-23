# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action set in a workbench window. """


from traits.api import Instance, List, Str

# Enthought library imports.
from envisage.ui.action.api import ActionSet


class WorkbenchActionSet(ActionSet):
    """An action set in a workbench window.

    This class adds a 'window' trait which is the workbench window that the
    action set is in. The trait is set by the framework when the action set is
    added to the window.

    It also adds a simple way for the action set to be enabled and/or visible
    in specific perspectives.

    """

    ###########################################################################
    # 'WorkbenchActionSet' interface.
    ###########################################################################

    # It is common for an action set to be enabled and/or visible only in a
    # particular perspective (or group of perspectives). The following traits
    # allow you to say which by specifiying a list of the appropriate
    # perspective *Ids*.
    #
    # For finer control over the enablement/visibility simply override the
    # 'initialize' method.
    enabled_for_perspectives = List(Str)
    visible_for_perspectives = List(Str)

    # It is common for an action set to be enabled and/or visible only when
    # particular view (or group of views) is visible. The following traits
    # allow you to say which by specifiying a list of the appropriate view
    # *Ids*.
    #
    # For finer control over the enablement/visibility simply override the
    # 'initialize' method.
    enabled_for_views = List(Str)
    visible_for_views = List(Str)

    # The workbench window that the action set is in.
    #
    # The framework sets this trait when the action set is first added to a
    # window.
    window = Instance("envisage.ui.workbench.api.WorkbenchWindow")

    ###########################################################################
    # 'ActionSet' interface.
    ###########################################################################

    def _enabled_changed(self, trait_name, old, new):
        """Static trait change handler."""

        if self.window is not None:
            self._update_tool_bars(self.window, "enabled", new)
            self._update_actions(self.window, "enabled", new)

    def _visible_changed(self, trait_name, old, new):
        """Static trait change handler."""

        if self.window is not None:
            self._update_tool_bars(self.window, "visible", new)
            self._update_actions(self.window, "visible", new)

    ###########################################################################
    # 'WorkbenchActionSet' interface.
    ###########################################################################

    def initialize(self):
        """Called when the action set has been added to a window.

        Use this method to hook up any listeners that you need to control
        the enabled and/or visible state of the action set.

        By default, we listen to the window being opened and the active
        perspective and active view being changed.

        """

        # We use dynamic trait handlers here instead of static handlers (or
        # @on_trait_change) because sub-classes might have a completely
        # different way to determine the anabled and/or visible state, hence
        # we might want to hook up completely different events.
        self.window.on_trait_change(self._refresh, "opened")
        self.window.on_trait_change(self._refresh, "active_part")
        self.window.on_trait_change(self._refresh, "active_perspective")

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _window_changed(self):
        """Static trait change handler."""

        # fixme: We put the code into an 'initialize' method because it seems
        # easier to explain that we expect it to be overridden. It seems a bit
        # smelly to say that a trait change handfler needs to be overridden.
        self.initialize()

    #### Methods ##############################################################

    def _refresh(self):
        """Refresh the enabled/visible state of the action set."""

        window = self.window

        if len(self.enabled_for_perspectives) > 0:
            self.enabled = (
                window is not None
                and window.active_perspective is not None
                and window.active_perspective.id
                in self.enabled_for_perspectives
            )

        if len(self.visible_for_perspectives) > 0:
            self.visible = (
                window is not None
                and window.active_perspective is not None
                and window.active_perspective.id
                in self.visible_for_perspectives
            )

        if len(self.enabled_for_views) > 0:
            self.enabled = (
                window is not None
                and window.active_part is not None
                and window.active_part.id in self.enabled_for_views
            )

        if len(self.visible_for_views) > 0:
            self.visible = (
                window is not None
                and window.active_part is not None
                and window.active_part.id in self.visible_for_views
            )

    def _update_actions(self, window, trait_name, value):
        """Update the state of the tool bars in the action set."""

        def visitor(item):
            """Called when we visit each item in an action manager."""

            # fixme: The 'additions' group gets created by default and hence
            # has no '_action_set_' attribute. This smells because of the fact
            # that we 'tag' the '_action_set_' attribute onto all items to be
            # ble to find them later. This link should be maintained externally
            # (maybe in the action set itself?).
            if hasattr(item, "_action_set_"):
                if item._action_set_ is self:
                    setattr(item, trait_name, value)

        # Update actions on the menu bar.
        window.menu_bar_manager.walk(visitor)

        # Update actions on the tool bars.
        for tool_bar_manager in window.tool_bar_managers:
            tool_bar_manager.walk(visitor)

    def _update_tool_bars(self, window, trait_name, value):
        """Update the state of the tool bars in the action set."""

        for tool_bar_manager in window.tool_bar_managers:
            if tool_bar_manager._action_set_ is self:
                setattr(tool_bar_manager, trait_name, value)
