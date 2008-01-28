""" A view that allows a developer to browse the current application. """


# Enthought library imports.
from enthought.pyface.workbench.api import TraitsUIView

# Local imports.
from application_browser import ApplicationBrowser


class ApplicationBrowserView(TraitsUIView):
    """ A view that allows a developer to browse the current application. """

    #### 'IWorkbenchPart' interface ###########################################
    
    # The part's globally unique identifier.
    id = 'enthought.envisage.ui.developer.view.application_browser_view'

    # The part's name (displayed to the user).
    name = 'Application Browser'

    ###########################################################################
    # 'TraitsUIView' interface.
    ###########################################################################

    def _obj_default(self):
        """ Trait initializer. """

        return ApplicationBrowser(application=self.window.application)

#### EOF ######################################################################
