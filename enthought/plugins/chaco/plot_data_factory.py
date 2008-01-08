""" Abstract base class for plot data factories. """


class PlotDataFactory(HasPrivateTraits):
    """ Abstract base class for plot data factories.

    A PlotDataFactory is responsible for decorating an object in a Chaco
    PlotData object in order for it to be plotted.

    Through the Envisage plotting plugin, subclasses of PlotDataFactory will
    be constructed by calling a no-argument constructor, so if a subclass
    implements a constructor method, it must take no arguments.
    """

    ###########################################################################
    # 'PlotDataFactory' interface.
    ###########################################################################

    def plot_data_for(self, obj):
        """ Return an enthought.chaco.PlotData which decorates obj. """

        raise NotImplementedError


#### EOF ######################################################################
