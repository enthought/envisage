""" The cookie required to enable the plot action. """


# Enthought library imports.
from enthought.envisage.project import Cookie


class PlotAsCookie(Cookie):
    """ The cookie required to enable the plot as action.

    The PlotAsCookie is only a marker cookie.  As such, developers of
    resource types that are plotted with templates need not extend this
    cookie.  Instead, they should contribute a plot template to the
    plotting plugin.
    
    """
    
#### EOF ######################################################################
