""" The Developer perspective. """


# Enthought library imports.
from pyface.workbench.api import Perspective, PerspectiveItem


class DeveloperPerspective(Perspective):
    """ The Developer perspective.

    This perspective is intented to contain views and editors useful for
    inspecting and debugging a running Envisage application.

    """

    # The root of all view Ids in this package.
    ROOT = 'envisage.developer.ui.view'

    # View Ids.
    APPLICATION_BROWSER_VIEW = ROOT + '.application_browser_view'
    EXTENSION_REGISTRY_BROWSER_VIEW = ROOT + '.extension_registry_browser_view'
    SERVICE_REGISTRY_BROWSER_VIEW = ROOT + '.service_registry_browser_view'

    # The perspective's name.
    name = 'Developer'

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        PerspectiveItem(
            id       = APPLICATION_BROWSER_VIEW,
            position = 'left'
        ),

        PerspectiveItem(
            id          = EXTENSION_REGISTRY_BROWSER_VIEW,
            position    = 'bottom',
            relative_to = APPLICATION_BROWSER_VIEW
        ),

        PerspectiveItem(
            id          = 'Python',
            position    = 'bottom',
        ),

        PerspectiveItem(
            id          = SERVICE_REGISTRY_BROWSER_VIEW,
            position    = 'right',
        ),
    ]

#### EOF ######################################################################
