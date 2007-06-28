""" An example traits UI view. """


# Enthought library imports.
from enthought.envisage.workbench.api import TraitsUIView
from enthought.traits.api import Int
from enthought.traits.ui.api import View


class ATraitsUIView(TraitsUIView):
    """ A example traits UI view. """

    view = View('x', 'y')

    #### 'ATraitsUIView' interface ############################################
    
    x = Int(10)
    y = Int(20)

#### EOF ######################################################################
