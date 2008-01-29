""" A view that allows a developer to browse the extension registry. """


# Enthought library imports.
from enthought.envisage.api import Service
from enthought.pyface.workbench.api import TraitsUIView


class ExtensionRegistryBrowserView(TraitsUIView):
    """ A view that allows a developer to browse the extension registry. """

    #### 'IWorkbenchPart' interface ###########################################
    
    # The part's globally unique identifier.
    id = 'enthought.envisage.developer.ui.view.extension_registry_browser_view'

    # The part's name (displayed to the user).
    name = 'Extension Points'

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
        from extension_registry_browser import ExtensionRegistryBrowser

        extension_registry_browser = ExtensionRegistryBrowser(
            application  = self.window.application,
            code_browser = self.code_browser
        )

        return extension_registry_browser

#### EOF ######################################################################
