""" A view that allows a developer to browse the current application. """


# Enthought library imports.
from enthought.envisage.api import Service
from enthought.pyface.workbench.api import TraitsUIView


class ApplicationBrowserView(TraitsUIView):
    """ A view that allows a developer to browse the current application. """

    #### 'IWorkbenchPart' interface ###########################################
    
    # The part's globally unique identifier.
    id = 'enthought.envisage.developer.ui.view.application_browser_view'

    # The part's name (displayed to the user).
    name = 'Plugins'

    #### 'ApplicationBrowserView' interface ###################################

    # The code browser used to parse Python code.
    code_browser = Service(
        'enthought.envisage.developer.code_browser.api.CodeBrowser'
    )

    ###########################################################################
    # 'TraitsUIView' interface.
    ###########################################################################

    def _obj_default(self):
        """ Trait initializer. """

        # Local imports.
        from application_browser import ApplicationBrowser

        application_browser = ApplicationBrowser(
            application  = self.window.application,
            code_browser = self.code_browser
        )

        return application_browser

#### EOF ######################################################################
