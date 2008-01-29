""" The developer UI plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class DeveloperUIPlugin(Plugin):
    """ The developer UI plugin.

    This plugin contains the UI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    # The plugin Id.
    ID = 'enthought.envisage.developer.ui'
    
    # Extension points Ids.
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    VIEWS        = 'enthought.envisage.ui.workbench.views'

    # View Ids.
    APPLICATION_BROWSER = ID + '.view.application_browser_view'

    #### 'IPlugin' interface ##################################################

    id   = ID
    name = 'Developer UI'

    #### Extension point contributions ########################################

    # Perspectives.
    perspectives = List(extension_point=PERSPECTIVES)

    # Views.
    views = List(extension_point=VIEWS)

    ###########################################################################
    # 'WorkbenchPlugin' interface.
    ###########################################################################

    def _views_default(self):
        """ Trait initializer. """

        from view.api import \
             ApplicationBrowserView, ExtensionRegistryBrowserView

        return [ApplicationBrowserView, ExtensionRegistryBrowserView]

    def _XXviews_default(self):
        """ Trait initializer. """

        # Enthought library imports.
        from enthought.pyface.workbench.api import TraitsUIViewFactory

        views = [
            TraitsUIViewFactory(
                id   = APPLICATION_BROWSER,
                name = 'Application Browser',
                obj  = self._create_application_browser()
            )
        ]

        return views

    def _perspectives_default(self):
        """ Trait initializer. """

        from enthought.envisage.developer.ui.perspective.api import \
             DeveloperPerspective

        return [DeveloperPerspective()]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_application_browser(self):
        """ Create an application browser. """

        # Local imports.
        from view.application_browser import ApplicationBrowser
        
        return ApplicationBrowser(application=self.application)
        
#### EOF ######################################################################
