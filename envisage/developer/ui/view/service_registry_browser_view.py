""" A view that allows a developer to browse the service registry. """


# Enthought library imports.
from pyface.workbench.api import TraitsUIView
from traits.api import Instance


# The code browser protocol.
CODE_BROWSER = 'envisage.developer.code_browser.api.CodeBrowser'


class ServiceRegistryBrowserView(TraitsUIView):
    """ A view that allows a developer to browse the service registry. """

    #### 'IWorkbenchPart' interface ###########################################

    # The part's globally unique identifier.
    id = 'envisage.developer.ui.view.service_registry_browser_view'

    # The part's name (displayed to the user).
    name = 'Services'

    #### 'IView' interface ####################################################

    # The category that the view belongs to (this can used to group views when
    # they are displayed to the user).
    category = 'Developer'

    #### 'ExtensionRegistryBrowserView' interface #############################

    # The code browser used to parse Python code.
    code_browser = Instance(CODE_BROWSER)

    ###########################################################################
    # 'TraitsUIView' interface.
    ###########################################################################

    def _obj_default(self):
        """ Trait initializer. """

        # Local imports.
        from .service_registry_browser import ServiceRegistryBrowser

        service_registry_browser = ServiceRegistryBrowser(
            application  = self.window.application,
            code_browser = self.code_browser
        )

        return service_registry_browser

    ###########################################################################
    # 'ServiceRegistryBrowserView' interface.
    ###########################################################################

    def _code_browser_default(self):
        """ Trait initializer. """

        return self.window.application.get_service(CODE_BROWSER)

#### EOF ######################################################################
