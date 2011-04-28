""" An action that dynamically creates and adds a view. """


# Enthought library imports.
from pyface.api import ImageResource
from pyface.action.api import Action
from pyface.workbench.api import View


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

        # You can give the view a position... (it default to 'left')...
        view = View(id='my.view.fred', name='Fred', position='right')
        self.window.add_view(view)

        # or you can specify it on the call to 'add_view'...
        view = View(id='my.view.wilma', name='Wilma')
        self.window.add_view(view, position='top')

        return

#### EOF ######################################################################
