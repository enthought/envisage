""" The cookie required to enable the plot action. """


# Enthought library imports.
from enthought.envisage.project import Cookie


class PlotCookie(Cookie):
    """ The cookie required to enable the plot action. """

    ##########################################################################
    # 'PlotCookie' interface.
    ##########################################################################

    def plot(self, window, bindings):
        """ Plot one or more of the bound resources.

        After the resources are plotted, they should be removed from bindings.
        This will allow other implementations to plot the remaining bindings, 
        and allows multiselection to not produce one plot window per selection.

        Subclasses which provide plotting behavior for resource types must
        implement this method appropriately.
        
        """

        raise NotImplementedError()

#### EOF ######################################################################
