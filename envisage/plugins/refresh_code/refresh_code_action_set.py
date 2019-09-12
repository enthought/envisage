# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
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
