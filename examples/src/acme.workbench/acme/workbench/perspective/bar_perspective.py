""" An example perspective. """


# Enthought library imports.
from enthought.pyface.workbench.api import Perspective, PerspectiveItem


class BarPerspective(Perspective):
    """ An example perspective. """

    name = 'Bar'
    show_editor_area = False

    contents = [
        PerspectiveItem(id='Green'),
        PerspectiveItem(id='Black', position='bottom', relative_to='Green')
    ]
    
#### EOF ######################################################################
