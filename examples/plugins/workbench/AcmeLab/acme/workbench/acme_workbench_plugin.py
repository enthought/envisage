""" The AcmeLab Workbench plugin. """


# Enthought library imports.
from envisage.api import Plugin
from traits.api import List


class AcmeWorkbenchPlugin(Plugin):
    """ The AcmeLab Workbench plugin.

    This plugin is part of the 'AcmeLab' example application.

    """

    # Extension points Ids.
    ACTION_SETS       = 'envisage.ui.workbench.action_sets'
    PERSPECTIVES      = 'envisage.ui.workbench.perspectives'
    PREFERENCES_PAGES = 'envisage.ui.workbench.preferences_pages'
    VIEWS             = 'envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.workbench'

    # The plugin's name (suitable for displaying to the user).
    name = 'Acme Workbench'

    #### Contributions to extension points made by this plugin ################

    # Action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """

        from test_action_set import TestActionSet

        return [TestActionSet]

    # Perspectives.
    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """ Trait initializer. """

        from acme.workbench.perspective.api import FooPerspective
        from acme.workbench.perspective.api import BarPerspective

        return [FooPerspective, BarPerspective]

    # Preferences pages.
    preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    def _preferences_pages_default(self):
        """ Trait initializer. """

        from acme_preferences_page import AcmePreferencesPage

        return [AcmePreferencesPage]

    # Views.
    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """ Trait initializer. """

        from acme.workbench.view.api import BlackView, BlueView, GreenView
        from acme.workbench.view.api import RedView, YellowView

        return [BlackView, BlueView, GreenView, RedView, YellowView]

#### EOF ######################################################################
