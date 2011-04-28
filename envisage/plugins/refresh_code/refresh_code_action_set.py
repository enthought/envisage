""" The default action set for the refresh code plugin. """


# Enthought library imports.
from envisage.ui.action.api import Action, ActionSet


# This package
PKG = '.'.join(__name__.split('.')[:-1])


refresh_code = Action(
    class_name = PKG + '.actions.RefreshCode',
    path       = 'MenuBar/Tools', group='additions'
)


class RefreshCodeActionSet(ActionSet):
    """ The default action set for the refresh code plugin. """

    actions = [refresh_code]

#### EOF ######################################################################
