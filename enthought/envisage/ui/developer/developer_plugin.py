""" The Developer plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class DeveloperPlugin(Plugin):
    """ The Developer plugin.

    This plugin contains views that (hopefully) help developers to inspect
    and debug a running Envisage workbench application.

    """

    # Extension points Ids.
    PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    VIEWS        = 'enthought.envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    id   = 'enthought.envisage.ui.developer'
    name = 'Developer'

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

        from enthought.envisage.ui.developer.view.api import ApplicationView
        
        return [ApplicationView]

    def _perspectives_default(self):
        """ Trait initializer. """

        from enthought.envisage.ui.developer.perspective.api import \
             DeveloperPerspective

        return [DeveloperPerspective()]

#### EOF ######################################################################
