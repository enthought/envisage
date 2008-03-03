""" An extensible workbench window. """


# Enthought library imports.
import enthought.pyface.workbench.api as pyface

from enthought.envisage.api import IApplication, ExtensionPoint
from enthought.envisage.ui.action.api import ActionSet
from enthought.pyface.workbench.api import IPerspective
from enthought.traits.api import Delegate, Instance, List, Property

# Local imports.
from workbench_action_manager_builder import WorkbenchActionManagerBuilder
from workbench_editor_manager import WorkbenchEditorManager


class WorkbenchWindow(pyface.WorkbenchWindow):
    """ An extensible workbench window. """

    # Extension point Ids.
    ACTION_SETS  = 'enthought.envisage.ui.workbench.actions'
    VIEWS        = 'enthought.envisage.ui.workbench.views'
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    
    #### 'WorkbenchWindow' interface ##########################################

    # The application that the view is part of.
    #
    # This is equivalent to 'self.workbench.application', and is provided just
    # as a convenience since windows often want access to the application.
    application = Delegate('workbench', modify=True)

    # The action sets that provide the toolbars, menus groups and actions
    # used in the window.
    action_sets = List(Instance(ActionSet))

    #### Private interface ####################################################

    # The workbench menu and tool bar builder.
    #
    # The builder is used to create the window's tool bar and menu bar by
    # combining all of the contributed action sets.
    _action_manager_builder = Instance(WorkbenchActionManagerBuilder)
    
    # Contributed action sets.
    _action_sets = ExtensionPoint(id=ACTION_SETS)
    
    # Contributed views (views are contributed as factories not view instances
    # as each workbench window requires its own).
    _views = ExtensionPoint(id=VIEWS)

    # Contributed perspectives.
    _perspectives = ExtensionPoint(id=PERSPECTIVES)

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

        return [factory(window=self) for factory in self._views]

    #### Methods ##############################################################

    def open(self):
        """ Open the window.

        Overridden to initialize the window's action sets once the window has
        been opened.

        """

        opened = super(WorkbenchWindow, self).open()
        if opened:
            self._initialize_action_sets()
            
        return opened
    
    ###########################################################################
    # 'WorkbenchWindow' interface.
    ###########################################################################

    def _action_sets_default(self):
        """ Trait initializer. """

        action_sets = []
        for factory_or_action_set in self._action_sets:
            if not isinstance(factory_or_action_set, ActionSet):
                action_set = factory_or_action_set()

            else:
                action_set = factory_or_action_set

            action_sets.append(action_set)

        return action_sets

    ###########################################################################
    # Private interface.
    ###########################################################################

    def __action_manager_builder_default(self):
        """ Trait initializer. """

        action_manager_builder = WorkbenchActionManagerBuilder(
            window=self, action_sets=self.action_sets
        )

        return action_manager_builder

    def _initialize_action_sets(self):
        """ Initialize all of the window's action sets.

        This gives the action sets a chance to enable/disable or show/hide
        menus, groups, tool bars or actions etc based on the initial state of
        the window.

        """
        
        for action_set in self.action_sets:
                action_set.initialize(self)

        return

#### EOF ######################################################################
