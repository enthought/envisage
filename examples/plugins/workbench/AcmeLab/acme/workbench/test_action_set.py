""" A test action set. """


# Enthought library imports.
from envisage.ui.action.api import Action, Group, Menu, ToolBar
from envisage.ui.workbench.api import WorkbenchActionSet


class TestActionSet(WorkbenchActionSet):
    """ An action test useful for testing. """

    #### 'ActionSet' interface ################################################

    # The action set's globally unique identifier.
    id = 'envisage.ui.workbench.test'

    menus = [
        Menu(
            name='&Test', path='MenuBar', before='Help',
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
            class_name='envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='MenuBar/Test', group='Fred',
            class_name='acme.workbench.action.new_view_action:NewViewAction'
        ),

        Action(
            path='ToolBar',
            class_name='envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='ToolBar',
            class_name='envisage.ui.workbench.action.api:ExitAction'
        ),

        Action(
            path='ToolBar/Fred', group='AToolBarGroup',
            class_name='envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='ToolBar/Wilma',
            class_name='envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='ToolBar/Barney',
            class_name='envisage.ui.workbench.action.api:ExitAction'
        )
    ]

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['Foo']

    # The Ids of the perspectives that the action set is visible in.
    visible_for_perspectives = ['Foo', 'Bar']

    # The Ids of the views that the action set is enabled for.
    #enabled_for_views = ['Red']

    # The Ids of the views that the action set is visible for.
    #visible_for_views = ['Red']

#### EOF ######################################################################
