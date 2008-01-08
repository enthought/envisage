""" An editor which edits a plot data object using its default plot. """

# Enthought library imports.
from enthought.chaco.plot_canvas import PlotCanvas
from enthought.chaco.plot_component import PlotComponent
from enthought.chaco.plot_data import PlotData
from enthought.envisage.ui import Editor
from enthought.traits.api import Instance


class PlotDataEditor(Editor):
    """ An editor which edits a plot data object using its default plot. """

    #### Trait definitions ####################################################
    
    plot_data = Instance(PlotData)

    
    ###########################################################################
    # 'Window' interface. 
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        plot_canvas = PlotCanvas(self.plot_data)
        plot_component = PlotComponent(component=canvas)

        # fixme : I think this will be enough... but if not, plot_component
        #         may need to be wrapped in a PlotWindow.

        return plot_component.control

#### EOF ######################################################################
