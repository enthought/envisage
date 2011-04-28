""" An example perspective. """


# Enthought library imports.
from pyface.workbench.api import Perspective, PerspectiveItem


class BarPerspective(Perspective):
    """ An example perspective. """

    # The perspective's name.
    name = 'Bar'

    # Should the editor area be shown in this perspective?
    show_editor_area = False

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id='Green'),
        PerspectiveItem(id='Black', position='bottom', relative_to='Green')
    ]

#### EOF ######################################################################
