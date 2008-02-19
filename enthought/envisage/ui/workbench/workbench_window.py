""" An extensible workbench window. """


# Enthought library imports.
import enthought.pyface.workbench.api as pyface

from enthought.envisage.api import IApplication, ExtensionPoint
from enthought.pyface.workbench.api import IPerspective
from enthought.traits.api import Instance, Property

# Local imports.
from workbench_action_manager_builder import WorkbenchActionManagerBuilder
from workbench_editor_manager import WorkbenchEditorManager


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
    
    # Contributed views (views are contributed as factories not view instances
    # as each workbench window requires its own).
    _view_factories = ExtensionPoint(id=VIEWS)

    # Contributed perspectives.
    _perspectives = ExtensionPoint(id=PERSPECTIVES)

    ###########################################################################
    # 'pyface.WorkbenchWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _editor_manager_default(self):
        """ Trait initializer. """

        return WorkbenchEditorManager(window=self)
    
    def _icon_default(self):
        """ Trait initializer. """

        return self.workbench.application.icon
    
    def _perspectives_default(self):
        """ Trait initializer. """

        perspectives = []
        for factory_or_perspective in self._perspectives:
            # Is the contribution an actual perspective, or is it a factory
            # that can create a perspective?
            perspective = IPerspective(factory_or_perspective, None)
            if perspective is None:
                perspective = factory_or_perspective()

            perspectives.append(perspective)
                
        return perspectives

    def _title_default(self):
        """ Trait initializer. """

        return self.workbench.application.name

    def _views_default(self):
        """ Trait initializer. """

        return [factory(window=self) for factory in self._view_factories]
    
    ###########################################################################
    # 'pyface.Window' interface.
    ###########################################################################

    #### Trait initializers ###################################################
    
    def _menu_bar_manager_default(self):
        """ Trait initializer. """

        return self._action_manager_builder.create_menu_bar_manager('MenuBar')

    def _tool_bar_managers_default(self):
        """ Trait initializer. """

        return self._action_manager_builder.create_tool_bar_managers('ToolBar')

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
