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
