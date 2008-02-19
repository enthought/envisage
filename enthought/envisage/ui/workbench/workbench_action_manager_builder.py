""" The action manager builder used to build the workbench menu/tool bars. """


# Standard library imports.
import weakref

# Enthought library imports.
from enthought.envisage.ui.action.api import AbstractActionManagerBuilder
from enthought.pyface.action.api import Action, Group, MenuManager
from enthought.pyface.workbench.action.api import ToolBarManager
from enthought.traits.api import Instance


class WorkbenchActionManagerBuilder(AbstractActionManagerBuilder):
    """ The action manager builder used to build the workbench menu/tool bars.

    """

    #### 'WorkbenchActionManagerBuilder' interface ############################

    # The workbench window that we build the menu and tool bars for.
    window = Instance('enthought.envisage.ui.workbench.api.WorkbenchWindow')

    #### Private CLASS interface ##############################################

    # All actions implementations.
    _actions = weakref.WeakValueDictionary()
    
    ###########################################################################
    # Protected 'MenuBuilder' interface.
    ###########################################################################

    def _create_action(self, definition):
        """ Create an action implementation from an action definition. """

        if len(definition.class_name) > 0:
            action = self._actions.get(definition.class_name)
            if action is None:
                klass  = self._import_symbol(definition.class_name)
                action = klass(window=self.window)
                self._actions[definition.class_name] = action
                
            # Overwrite any attributes specified in the definition.
            #
            # fixme: Is there a better way to do this?
            if len(definition.name) > 0:
                action.name = definition.name

        else:
            action = Action(name=definition.name)

        return action

    def _create_group(self, definition):
        """ Create a group implementation from a group definition. """

        if len(definition.class_name) > 0:
            klass = self._import_symbol(definition.class_name)
            group = klass()

            # Overwrite any attributes specified in the definition.
            #
            # fixme: Is there a better way to do this?
            if len(definition.id) > 0:
                group.id = definition.id

        else:
            group = Group(id=definition.id)

        return group

    def _create_menu_manager(self, definition):
        """ Create a menu manager implementation from a menu definition. """

        if len(definition.class_name) > 0:
            klass = self._import_symbol(definition.class_name)

            # fixme: 'window' is not actually a trait on 'MenuManager'! We set
            # it here to allow the 'View' menu to be created. However, it seems
            # that menus and actions etc should *always* have a reference to
            # the window that they are in?!?
            menu_manager = klass(window=self.window)

            # Overwrite any attributes specified in the definition.
            #
            # fixme: Is there a better way to do this?
            if len(definition.name) > 0:
                menu_manager.name = definition.name
            
        else:
            menu_manager = MenuManager(
                window=self.window, id=definition.id, name=definition.name
            )
            
        # Add any groups to the menu.
        for group in definition.groups:
            menu_manager.insert(-1, self._create_group(group))

        return menu_manager

    def _create_tool_bar_manager(self, definition):
        """ Create a tool bar manager implementation from a definition. """

        if len(definition.class_name) > 0:
            klass = self._import_symbol(definition.class_name)
            
            # fixme: 'window' is not actually a trait on 'ToolBarManager'! We
            # set it here because it is set on the 'MenuManager'! However, it
            # seems that menus and actions etc should *always* have a reference
            # to the window that they are in?!?
            tool_bar_manager = klass(window=self.window)

            # Overwrite any attributes specified in the definition.
            #
            # fixme: Is there a better way to do this?
            if len(definition.name) > 0:
                tool_bar_manager.name = definition.name
            
        else:
            tool_bar_manager = ToolBarManager(
                id              = definition.id,
                name            = definition.name,
                show_tool_names = False,
                window          = self.window
            )
            
        # Add any groups to the menu.
        for group in definition.groups:
            tool_bar_manager.insert(-1, self._create_group(group))

        return tool_bar_manager

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _import_symbol(self, symbol_path):
        """ Import a symbol. """

        return self.window.application.import_symbol(symbol_path)
    
#### EOF ######################################################################
