""" An action set is a collection of menus, groups, and actions. """


# Enthought library imports.
from enthought.traits.api import Bool, Dict, HasTraits, List, Str, implements
from enthought.traits.api import on_trait_change

# Local imports.
from action import Action
from group import Group
from i_action_set import IActionSet
from menu import Menu
from tool_bar import ToolBar


class ActionSet(HasTraits):
    """ An action set is a collection of menus, groups, and actions. """

    implements(IActionSet)
    
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

    # Are the actions and menus in this set enabled (if they are diabled they
    # will be greyed out).
    enabled = Bool(True)

    # Are the actions, menus and toolbars in this set visible?
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
    # ``'enthought.envisage.workbench.menubar'``
    #
    # Without aliases, you must specify a location like this:
    #
    # ``Location(path='enthought.envisage.workbench.menubar/ASubMenu/AGroup')``
    #
    # This is a bit long-winded! Instead, you can define an alias:
    #
    #     ``aliases = { 'MenuBar' : 'enthought.envisage.workbench.menubar' }``
    #
    # In that case, you can specify a location like this:
    #
    #     ``Location(path='MenuBar/ASubMenu/AGroup')``
    #
    aliases = Dict(Str, Str)

    ###########################################################################
    # 'ActionSet' interface.
    ###########################################################################

##     @on_trait_change('enabled,visible')
##     def _state_changed(self, obj, trait_name, old, new):
##         """ Static trait change handler. """

##         self._update_tool_bars(obj, trait_name, new)
##         self._update_actions(obj, trait_name, new)

##         return

    def initialize(self, window):
        """ Called by the framework when the action set is added to a window.

        """



        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _update_tool_bars(self, window, trait_name, value):
        """ Update the state of the tool bars in the action set. """

        for tool_bar_manager in window.tool_bar_managers:
            if tool_bar_manager._action_set_ is action_set:
                setattr(tool_bar_manager, trait_name, value)

        return

    def _update_actions(self, window, trait_name, value):
        """ Update the state of the tool bars in the action set. """

        def visitor(item):
            """ Called when we visit each item in an action manager. """

            # fixme: The 'additions' group gets created by default and hence
            # has no '_action_set_' attribute. This smells because of the
            # fact that we 'tag' the '_action_set_' attribute onto all items to
            # be able to find them later. This link should be maintained
            # externally (maybe in the action set itself?).
            if hasattr(item, '_action_set_'):
                if item._action_set_ is action_set:
                    setattr(item, trait_name, value)

        window.menu_bar_manager.walk(visitor)

        for tool_bar_manager in window.tool_bar_managers:
            tool_bar_manager.walk(visitor)

        return

    ###########################################################################
    # Testing interface.
    ###########################################################################

    def test(self):
        """ Testing! """

        pass
    
#### EOF ######################################################################
