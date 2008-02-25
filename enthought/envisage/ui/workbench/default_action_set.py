""" The default workbench action set. """


# Enthought library imports.
from enthought.envisage.ui.action.api import Action, ActionSet, Menu


class DefaultActionSet(ActionSet):
    """ The default workbench action set. """

    id = 'enthought.envisage.ui.workbench.default'
    
    menus = [
        Menu(
            name='&File', path='MenuBar',
            groups=['OpenGroup', 'SaveGroup', 'ImportGroup', 'ExitGroup']
        ),

        Menu(
            path='MenuBar',
            class_name='enthought.pyface.workbench.action.api:ViewMenuManager'
        ),

        Menu(
            name='&Tools', path='MenuBar',
            groups=['PreferencesGroup']
        ),
        
        Menu(
            name='&Help', path='MenuBar',
            groups=['AboutGroup']
        )
    ]

    actions = [
        Action(
            path='MenuBar/File', group='ExitGroup',
            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
        ),

        Action(
            path='MenuBar/Tools', group='PreferencesGroup',
            class_name='enthought.envisage.ui.workbench.action.api:EditPreferencesAction'
        ),
        
        Action(
            path='MenuBar/Help', group='AboutGroup',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),
    ]

#### EOF ######################################################################
