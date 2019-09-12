# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Actions for the refresh code plugin. """


# Enthought library imports.
from pyface.action.api import Action


class RefreshCode(Action):
    """ Invoke the 'refresh code' function. """

    #### 'Action' interface ###################################################

    name        = 'Refresh Code'
    description = 'Refresh application to reflect python code changes'
    accelerator = 'Ctrl+Shift+R'

    def perform(self, event):
        """ Perform the action. """

        from traits.util.refresh import refresh

        refresh()

        return

#### EOF ######################################################################
