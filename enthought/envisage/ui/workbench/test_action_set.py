""" A test action set. """


# Enthought library imports.
from enthought.envisage.ui.action.api import Action, Group, Menu, ToolBar
from enthought.envisage.ui.workbench.api import WorkbenchActionSet


class TestActionSet(WorkbenchActionSet):
    """ An action test useful for testing. """

    #### 'ActionSet' interface ################################################
    
    # The action set's globally unique identifier.
    id = 'enthought.envisage.ui.workbench.test'

    menus = [
        Menu(
            name='&Test', path='MenuBar',
            groups=['XGroup', 'YGroup']
        ),

        Menu(
            name='Foo', path='MenuBar/Test',
            groups=['XGroup', 'YGroup']
        ),

        Menu(
            name='Bar', path='MenuBar/Test',
            groups=['XGroup', 'YGroup']
        ),
    ]

    groups = [
        Group(id='Fred', path='MenuBar/Test')
    ]
        
    tool_bars = [
        ToolBar(name='Fred', groups=['AToolBarGroup']),
        ToolBar(name='Wilma'),
        ToolBar(name='Barney')
    ]
        
    actions = [
        Action(
            path='MenuBar/Test', group='Fred',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='ToolBar',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),
        
        Action(
            path='ToolBar',
            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
        ),

        Action(
            path='ToolBar/Fred', group='AToolBarGroup',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='ToolBar/Wilma',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),
        
        Action(
            path='ToolBar/Barney',
            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
        )
    ]

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_in = ['Foo']

    # The Ids of the perspectives that the action set is visible in.
    visible_in = ['Foo', 'Bar']

#### EOF ######################################################################
