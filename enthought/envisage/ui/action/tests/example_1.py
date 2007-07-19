""" A test action set. """


# Enthought library imports.
from enthought.envisage.ui.action.api import Action, ActionSet, Group, Location
from enthought.envisage.ui.action.api import Menu


action_set = ActionSet(
##     id   = ID + '.default_action_set',
##     name = 'Default',


    groups = [
        Group(
            id = 'BazMenuGroup',
            location = Location(path='MenuBar', after='BarMenuGroup')
        ),
        
        Group(
            id = 'BarMenuGroup',
            location = Location(path='MenuBar', after='FooMenuGroup')
        ),

        Group(
            id = 'HelpMenuGroup',
            location = Location(path='MenuBar', after='FileMenuGroup')
        ),

        Group(
            id = 'FileMenuGroup',
            location = Location(path='MenuBar')
        ),

        Group(
            id = 'FooMenuGroup',
            location = Location(path='MenuBar', before='FileMenuGroup')
        ),

    ],

    menus = [
        Menu(
            id = 'BazMenu',
            name = 'B&az',
            location = Location(path='MenuBar/BazMenuGroup'),
        ),

        Menu(
            id = 'FileMenu',
            name = '&File',
            location = Location(path='MenuBar'),

            groups = [
                Group(id='ExitGroup')
            ]
        ),

        Menu(
            id = 'Foo2Menu',
            name = 'Foo&2',
            location = Location(path='MenuBar/FooMenuGroup', after='Foo1Menu'),
        ),

        Menu(
            id = 'Foo1Menu',
            name = 'Foo&1',
            location = Location(path='MenuBar/FooMenuGroup', after='FooMenu'),
        ),

        Menu(
            id = 'BarMenu',
            name = '&Bar',
            location = Location(path='MenuBar/BarMenuGroup'),
        ),

        Menu(
            id = 'FooMenu',
            name = 'F&oo',
            location = Location(path='MenuBar/FooMenuGroup'),
        ),


        Menu(
            id = 'HelpMenu',
            name = '&Help',
            location = Location(path='MenuBar/HelpMenuGroup'),

            groups = [
                Group(id='AboutGroup')
            ]
        )
    ],

    actions = [
        Action(
            class_name = 'acme.action.exit_action:ExitAction',
            locations = [
                Location(path='MenuBar/FileMenu/ExitGroup')
            ]
        ),

        Action(
            class_name = 'acme.action.about_action:AboutAction',
            locations = [
                Location(path='MenuBar/HelpMenu/AboutGroup')
            ]
        )
    ]
)

#### EOF ######################################################################


