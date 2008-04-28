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

    # The plugin's unique identifier.
    id   = ID

    # The plugin's name (suitable for displaying to the user).
    name = 'Developer UI'

    #### 'DeveloperUIPlugin' interface ########################################

    #### Extension points offered by this plugin ##############################

    # None.

    #### Contributions to extension points made by this plugin ################

    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """ Trait initializer. """

        from enthought.envisage.developer.ui.perspective.api import (
            DeveloperPerspective
        )

        return [DeveloperPerspective]

    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """ Trait initializer. """

        from view.api import (
            ApplicationBrowserView,
            ExtensionRegistryBrowserView,
            ServiceRegistryBrowserView
        )

        views = [
            ApplicationBrowserView,
            ExtensionRegistryBrowserView,
            ServiceRegistryBrowserView
        ]

        return views

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_application_browser(self):
        """ Create an application browser. """

        # Local imports.
        from view.application_browser import ApplicationBrowser
        
        return ApplicationBrowser(application=self.application)
        
#### EOF ######################################################################
