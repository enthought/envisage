""" The Developer perspective. """


# Enthought library imports.
from enthought.pyface.workbench.api import Perspective, PerspectiveItem


class DeveloperPerspective(Perspective):
    """ The Developer perspective.

    This perspective is intented to contain views and editors useful for
    inspecting and debugging a running Envisage application.

    """

    # The root of all view Ids in this package.
    ROOT = 'enthought.envisage.ui.developer.view'

    # View Ids.
    APPLICATION_BROWSER_VIEW = ROOT + '.application_browser_view'
    
    # The perspective's name.
    name = 'Developer'

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id=APPLICATION_BROWSER_VIEW,  position='left'),
    ]
    
#### EOF ######################################################################
