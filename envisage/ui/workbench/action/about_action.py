# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An action that shows the 'About' dialog. """


# Enthought library imports.
from pyface.action.api import Action


class AboutAction(Action):
    """ An action that shows the 'About' dialog. """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Display information about the application'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'About'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Display information about the application'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        self.window.application.about()

        return

#### EOF ######################################################################
