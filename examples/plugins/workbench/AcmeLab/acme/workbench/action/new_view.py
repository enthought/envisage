""" An action that dynamically creates and adds a view. """


# Enthought library imports.
from pyface.action.api import Action


class NewViewAction(Action):
    """ An action that dynamically creates and adds a view. """

    #### 'Action' interface ###################################################

    # A longer description of the action.
    description = 'Create and add a new view'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'New View'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Create and add a new view'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        # Create your view...
        view = View(id='my.view.fred', name='Fred', position='right')

        # ... add it to the window!
        self.window.add_view(view)

        return

#### EOF ######################################################################
