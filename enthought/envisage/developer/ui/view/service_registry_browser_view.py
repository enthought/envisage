""" A view that allows a developer to browse the service registry. """


# Enthought library imports.
from enthought.envisage.api import Service
from enthought.pyface.workbench.api import TraitsUIView


class ServiceRegistryBrowserView(TraitsUIView):
    """ A view that allows a developer to browse the service registry. """

    #### 'IWorkbenchPart' interface ###########################################
    
    # The part's globally unique identifier.
    id = 'enthought.envisage.developer.ui.view.service_registry_browser_view'

    # The part's name (displayed to the user).
    name = 'Services'

    #### 'ExtensionRegistryBrowserView' interface #############################

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
        from service_registry_browser import ServiceRegistryBrowser

        service_registry_browser = ServiceRegistryBrowser(
            application  = self.window.application,
            code_browser = self.code_browser
        )

        return service_registry_browser

#### EOF ######################################################################
