""" The AcmeLab Workbench plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class WorkbenchPlugin(Plugin):
    """ The AcmeLab Workbench plugin.

    This plugin is part of the 'AcmeLab' example application.

    """

    # Extension points Ids.
    PERSPECTIVES      = 'enthought.envisage.ui.workbench.perspectives'
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'
    VIEWS             = 'enthought.envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    id   = 'acme.workbench'
    name = 'Acme Workbench'

    #### Extension point contributions ########################################

    # Perspectives.
    perspectives = List(extension_point=PERSPECTIVES)

    # Views.
    views = List(extension_point=VIEWS)

    # Preferences pages.
    preferences_pages = List(extension_point=PREFERENCES_PAGES)

    ###########################################################################
    # 'WorkbenchPlugin' interface.
    ###########################################################################

    def _views_default(self):
        """ Trait initializer. """

        from acme.workbench.view.api import BlackView, BlueView, GreenView
        from acme.workbench.view.api import RedView, YellowView
        
        return [BlackView, BlueView, GreenView, RedView, YellowView]

    def _perspectives_default(self):
        """ Trait initializer. """

        from acme.workbench.perspective.api import FooPerspective
        from acme.workbench.perspective.api import BarPerspective

        return [FooPerspective(), BarPerspective()]

    def _preferences_pages_default(self):
        """ Trait initializer. """

        from acme_preferences_page import AcmePreferencesPage
        
        return [AcmePreferencesPage()]

#### EOF ######################################################################
