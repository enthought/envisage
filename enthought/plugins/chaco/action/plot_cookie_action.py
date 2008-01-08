""" Cookie action for plotting resources. """

# Standard library imports.
import logging


# Enthought library imports.
from enthought.envisage.project import CookieAction, CookieManager

# Local imports.
from enthought.plugins.chaco.cookie.plot_cookie import PlotCookie


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class PlotCookieAction(CookieAction):
    """ Cookie action for plotting resources. """

    #### 'CookieAction' interface #############################################

    # Require the plot cookie to plot.
    required_cookie = PlotCookie

    #### 'Action' interface ###################################################

    description = 'Plot the resource.'

    id = 'enthought.plugins.chaco.plot_cookie_action'

    name = 'Plot...'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self):
        """ Performs the action. """

        # FIXME!
        cm = CookieManager()

        bindings = self.window.selection[:]
        while len(bindings) > 0:
            cookie = cm.get_cookie(self.required_cookie, bindings[0].obj)

            # If there is a plot cookie for the first binding, invoke it.
            if cookie is not None:
                starting_length = len(bindings)
                cookie.plot(self.window, bindings)

                # Protect ourselves from a cookie that does not remove the
                # bindings that it consumed.  Warn the user and remove the
                # first binding which was used to locate the cookie.
                if starting_length == len(bindings):
                    logger.warning(
                        'PlotCookie %s failed to remove bindings.' % cookie
                    )
                    del bindings[0]

            # Otherwise, if there is not a plot cookie for the first binding,
            # then just remove it from the set of bindings.
            else:
                del bindings[0]

        return

#### EOF ######################################################################
