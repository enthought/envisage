""" An example perspective. """


# Enthought library imports.
from enthought.pyface.workbench.api import Perspective, PerspectiveItem


class FooPerspective(Perspective):
    """ An example perspective. """

    name = 'Foo'

    contents = [
        PerspectiveItem(id='Blue', position='left'),
        PerspectiveItem(id='Red', position='with', relative_to='Blue'),
        PerspectiveItem(id='Green', position='top')
    ]
    
#### EOF ######################################################################
