# (C) Copyright 2007-2024 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The AcmeLab Workbench plugin. """


from traits.api import List

# Enthought library imports.
from envisage.api import Plugin


class AcmeWorkbenchPlugin(Plugin):
    """The AcmeLab Workbench plugin.

    This plugin is part of the 'AcmeLab' example application.

    """

    # Extension points Ids.
    ACTION_SETS = "envisage.ui.workbench.action_sets"
    PERSPECTIVES = "envisage.ui.workbench.perspectives"
    PREFERENCES_PAGES = "envisage.ui.workbench.preferences_pages"
    VIEWS = "envisage.ui.workbench.views"

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = "acme.workbench"

    # The plugin's name (suitable for displaying to the user).
    name = "Acme Workbench"

    #### Contributions to extension points made by this plugin ################

    # Action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """Trait initializer."""

        from .example_action_set import ExampleActionSet

        return [ExampleActionSet]

    # Perspectives.
    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """Trait initializer."""

        from acme.workbench.perspective.api import (
            BarPerspective,
            FooPerspective,
        )

        return [FooPerspective, BarPerspective]

    # Preferences pages.
    preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    def _preferences_pages_default(self):
        """Trait initializer."""

        from acme_preferences_page import AcmePreferencesPage

        return [AcmePreferencesPage]

    # Views.
    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """Trait initializer."""

        from acme.workbench.view.api import (
            BlackView,
            BlueView,
            GreenView,
            RedView,
            YellowView,
        )

        return [BlackView, BlueView, GreenView, RedView, YellowView]
