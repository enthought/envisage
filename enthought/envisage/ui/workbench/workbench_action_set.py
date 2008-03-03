""" An action set in a workbench window. """


# Enthought library imports.
from enthought.envisage.ui.action.api import ActionSet
from enthought.traits.api import Instance, List, Str, on_trait_change


class WorkbenchActionSet(ActionSet):
    """ An action set in a workbench window.

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
    enabled_in = List(Str)
    visible_in = List(Str)
    
    # The workbench window that the action set is in.
    #
    # The framework sets this trait when the action set is first added to a
    # window.
    window = Instance('enthought.envisage.ui.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'ActionSet' interface.
    ###########################################################################

    def _enabled_changed(self, trait_name, old, new):
        """ Static trait change initializer. """

        if self.window is not None:
            self._update_tool_bars(self.window, 'enabled', new)
            self._update_actions(self.window, 'enabled', new)

        return

    def _visible_changed(self, trait_name, old, new):
        """ Static trait change initializer. """

        if self.window is not None:
            self._update_tool_bars(self.window, 'visible', new)
            self._update_actions(self.window, 'visible', new)

        return

    ###########################################################################
    # 'WorkbenchActionSet' interface.
    ###########################################################################
    
    @on_trait_change('window:[opened,active_perspective]')
    def refresh(self):
        """ Refresh the enabled/visible state of the action set. """

        window = self.window

        if len(self.enabled_in) > 0:
            self.enabled = window is not None \
                           and window.active_perspective is not None \
                           and window.active_perspective.id in self.enabled_in

        if len(self.visible_in) > 0:
            self.visible = window is not None \
                           and window.active_perspective is not None \
                           and window.active_perspective.id in self.visible_in

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _update_actions(self, window, trait_name, value):
        """ Update the state of the tool bars in the action set. """

        def visitor(item):
            """ Called when we visit each item in an action manager. """

            # fixme: The 'additions' group gets created by default and hence
            # has no '_action_set_' attribute. This smells because of the fact
            # that we 'tag' the '_action_set_' attribute onto all items to be
            # ble to find them later. This link should be maintained externally
            # (maybe in the action set itself?).
            if hasattr(item, '_action_set_'):
                if item._action_set_ is self:
                    setattr(item, trait_name, value)

            return
        
        # Update actions on the menu bar.
        window.menu_bar_manager.walk(visitor)

        # Update actions on the tool bars.
        for tool_bar_manager in window.tool_bar_managers:
            tool_bar_manager.walk(visitor)

        return
    
    def _update_tool_bars(self, window, trait_name, value):
        """ Update the state of the tool bars in the action set. """

        for tool_bar_manager in window.tool_bar_managers:
            if tool_bar_manager._action_set_ is self:
                setattr(tool_bar_manager, trait_name, value)

        return

#### EOF ######################################################################
