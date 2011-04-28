""" An example perspective. """


# Enthought library imports.
from pyface.workbench.api import Perspective, PerspectiveItem


class FooPerspective(Perspective):
    """ An example perspective. """

    # The perspective's name.
    name = 'Foo'

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id='Blue',  position='left'),
        PerspectiveItem(id='Red',   position='with', relative_to='Blue'),
        PerspectiveItem(id='Green', position='top')
    ]

#### EOF ######################################################################
