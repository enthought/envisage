""" The developer UI plugin. """


# Enthought library imports.
from envisage.api import Plugin
from traits.api import List


class DeveloperUIPlugin(Plugin):
    """ The developer UI plugin.

    This plugin contains the UI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    # The plugin Id.
    ID = 'envisage.developer.ui'

    # Extension points Ids.
    PERSPECTIVES = 'envisage.ui.workbench.perspectives'
    VIEWS        = 'envisage.ui.workbench.views'

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

        from envisage.developer.ui.perspective.api import (
            DeveloperPerspective
        )

        return [DeveloperPerspective]

    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """ Trait initializer. """

        from .view.api import (
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

#### EOF ######################################################################
