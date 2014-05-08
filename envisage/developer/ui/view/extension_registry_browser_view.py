""" A view that allows a developer to browse the extension registry. """


# Enthought library imports.
from pyface.workbench.api import TraitsUIView
from traits.api import Instance


# The code browser protocol.
CODE_BROWSER = 'envisage.developer.code_browser.api.CodeBrowser'


class ExtensionRegistryBrowserView(TraitsUIView):
    """ A view that allows a developer to browse the extension registry. """

    #### 'IWorkbenchPart' interface ###########################################

    # The part's globally unique identifier.
    id = 'envisage.developer.ui.view.extension_registry_browser_view'

    # The part's name (displayed to the user).
    name = 'Extension Points'

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
        from .extension_registry_browser import ExtensionRegistryBrowser

        extension_registry_browser = ExtensionRegistryBrowser(
            application  = self.window.application,
            code_browser = self.code_browser
        )

        return extension_registry_browser

    ###########################################################################
    # 'ExtensionRegistryBrowserView' interface.
    ###########################################################################

    def _code_browser_default(self):
        """ Trait initializer. """

        return self.window.application.get_service(CODE_BROWSER)

#### EOF ######################################################################
