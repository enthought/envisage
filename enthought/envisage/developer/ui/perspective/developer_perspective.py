""" The Developer perspective. """


# Enthought library imports.
from enthought.pyface.workbench.api import Perspective, PerspectiveItem


class DeveloperPerspective(Perspective):
    """ The Developer perspective.

    This perspective is intented to contain views and editors useful for
    inspecting and debugging a running Envisage application.

    """

    APPLICATION_VIEW = 'enthought.envisage.ui.developer.view.application_view'
    
    # The perspective's name.
    name = 'Developer'

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id=APPLICATION_VIEW,  position='left'),
    ]
    
#### EOF ######################################################################
