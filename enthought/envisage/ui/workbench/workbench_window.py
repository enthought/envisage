""" An extensible workbench window. """


# Enthought library imports.
import enthought.pyface.workbench.api as pyface

from enthought.envisage.api import IApplication, ExtensionPoint
from enthought.envisage.ui.action.api import ActionSet
from enthought.pyface.workbench.action.api import MenuBarManager
from enthought.pyface.workbench.action.api import ToolBarManager
from enthought.traits.api import Callable, Instance, List, Property

# Local imports.
from workbench_action_manager_builder import WorkbenchActionManagerBuilder


class WorkbenchWindow(pyface.WorkbenchWindow):
    """ An extensible workbench window. """

    # Extension point Ids.
    ACTIONS      = 'enthought.envisage.ui.workbench.actions'
    VIEWS        = 'enthought.envisage.ui.workbench.views'
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    
    #### 'WorkbenchWindow' interface ##########################################

    # The application that the view is part of.
    #
    # This is equivalent to 'self.workbench.application', and is provided just
    # as a convenience since windows often want access to the application.
    application = Property(Instance(IApplication))

    #### Private interface ####################################################

    # The workbench menu and tool bar builder.
    _action_manager_builder = Instance(WorkbenchActionManagerBuilder)
    
    # Contributed action sets.
    _actions = ExtensionPoint(id=ACTIONS)
    
    # Contributed views.
    _views = ExtensionPoint(id=VIEWS)

    # Contributed perspectives.
    _perspectives = ExtensionPoint(id=PERSPECTIVES)

    ###########################################################################
    # 'pyface.WorkbenchWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _icon_default(self):
        """ Trait initializer. """

        return self.workbench.application.icon
    
    def _perspectives_default(self):
        """ Trait initializer. """

        import inspect
        
        perspectives = []
        for perspective in self._perspectives:
            if inspect.isclass(perspective):
                perspectives.append(perspective())

            else:
                perspectives.append(perspective)
                
        return perspectives

    def _title_default(self):
        """ Trait initializer. """

        return self.workbench.application.name

    def _views_default(self):
        """ Trait initializer. """

        import inspect
        
        views = []
        for view in self._views:
            if inspect.isclass(view):
                views.append(view(window=self))

            else:
                view.window = self
                views.append(view)
                
        return views
    
    ###########################################################################
    # 'pyface.Window' interface.
    ###########################################################################

    #### Trait initializers ###################################################
    
    def _menu_bar_manager_default(self):
        """ Trait initializer. """

        # Create an empty menu bar.
        menu_bar_manager = MenuBarManager(window=self)

        # Add all of the contributed menus, groups and actions.
        self._action_manager_builder.initialize_action_manager(
            menu_bar_manager, 'MenuBar'
        )

        return menu_bar_manager

    def _tool_bar_manager_default(self):
        """ Trait initializer. """

        # Create an empty tool bar.
        tool_bar_manager = ToolBarManager(window=self, show_tool_names=False)

        # Add all of the contributed groups and actions.
        self._action_manager_builder.initialize_action_manager(
            tool_bar_manager, 'ToolBar'
        )

        return tool_bar_manager

    ###########################################################################
    # 'WorkbenchWindow' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_application(self):
        """ Property getter. """

        return self.workbench.application

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def __action_manager_builder_default(self):
        """ Trait initializer. """

        import inspect
        
        actions = []
        for action in self._actions:
            if inspect.isclass(action):
                actions.append(action())

            else:
                actions.append(action)
        
        return WorkbenchActionManagerBuilder(window=self, action_sets=actions)
    
#### EOF ######################################################################
