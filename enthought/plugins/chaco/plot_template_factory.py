""" Factory for producing templated plot components. """

from enthought.traits.api import HasPrivateTraits


class PlotTemplateFactory(HasPrivateTraits):
    """ Factory for producing templated plot components. """
    
    def create_plot_editor(self, selection, parent):
        """ Return a chaco PlotComponent that plots the selection.

        Contributed template factories must override this method.
        """

        raise NotImplementedError


#### EOF ######################################################################
