""" A PlotCookie which uses a PlotDataFactory. """


# Local imports.
from plot_cookie import PlotCookie
from plot_data_editor import PlotDataEditor
from plot_data_manager import PlotDataManager


class PlotDataCookie(PlotCookie):
    """ A PlotCookie which uses a PlotDataFactory.

    To plot an object, the PlotDataCookie looks up the PlotDataFactory for the
    resource type, constructs a PlotData, and plots it.
    """

    ###########################################################################
    # 'PlotData' interface.
    ###########################################################################

    def plot(self, window, resource):
        """ Plot the resource. """

        plot_data_manager = PlotDataManager()
        try:
            ### FIXME : We probably need to do something about getting the
            ###         resource from the object. :-(

            factory = plot_data_manager.get_plot_data_factory(resource)

            plot_data = factory.plot_data_for(resource)

            # Create and show the editor.
            editor = self._plot_editor_for(plot_data)
            editor.open()

        except:
            # fixme : log this!
            pass

    ###########################################################################
    # Private interface.
    ###########################################################################

    # fixme : do we really need this method?
    def _plot_editor_for(self, plot_data):
        """ Create a plot editor for the specified PlotData object. """

        return PlotDataEditor(plot_data=plot_data)

#### EOF ######################################################################
