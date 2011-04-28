""" The default workbench action set. """


# Enthought library imports.
from envisage.ui.action.api import Action, ActionSet, Menu


# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])


class DefaultActionSet(ActionSet):
    """ The default workbench action set. """

    menus = [
        Menu(
            name='&File', path='MenuBar',
            groups=['OpenGroup', 'SaveGroup', 'ImportGroup', 'ExitGroup']
        ),

        Menu(
            path='MenuBar',
            class_name='pyface.workbench.action.api:ViewMenuManager'
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
            class_name=PKG + '.action.api:ExitAction'
        ),

        Action(
            path='MenuBar/Tools', group='PreferencesGroup',
            class_name=PKG + '.action.api:EditPreferencesAction'
        ),

        Action(
            path='MenuBar/Help', group='AboutGroup',
            class_name=PKG + '.action.api:AboutAction'
        ),
    ]

#### EOF ######################################################################
