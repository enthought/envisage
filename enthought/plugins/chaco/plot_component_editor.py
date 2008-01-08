""" An editor which edits a plot data object using its default plot. """

# Enthought library imports.
from enthought.chaco.plot_canvas import PlotCanvas
from enthought.chaco.plot_component import PlotComponent
from enthought.chaco.plot_data import PlotData
from enthought.envisage.ui import Editor
from enthought.traits.api import Instance


class PlotComponentEditor(Editor):
    """ An editor which edits a plot data object using its default plot. """

    #### Trait definitions ####################################################
    
    plot_component = Instance(PlotComponent)

    
    ###########################################################################
    # 'Window' interface. 
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        return self.plot_component.control

#### EOF ######################################################################
