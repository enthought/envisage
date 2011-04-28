""" The Lorenz example application. """


# Standard library imports.
from logging import DEBUG

# Enthought library imports.
from envisage.ui.workbench.api import WorkbenchApplication
from pyface.api import AboutDialog, ImageResource, SplashScreen


class LorenzApplication(WorkbenchApplication):
    """ The Lorenz example application. """

    #### 'IApplication' interface #############################################

    # The application's globally unique Id.
    id = 'acme.lorenz'

    #### 'WorkbenchApplication' interface #####################################

    # Branding information.
    #
    # The icon used on window title bars etc.
    icon = ImageResource('lorenz.ico')

    # The name of the application (also used on window title bars etc).
    name = 'Lorenz'

    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    def _about_dialog_default(self):
        """ Trait initializer. """

        about_dialog = AboutDialog(
            parent = self.workbench.active_window.control,
            image  = ImageResource('about')
        )

        return about_dialog

    def _splash_screen_default(self):
        """ Trait initializer. """

        splash_screen = SplashScreen(
            image             = ImageResource('splash'),
            show_log_messages = True,
            log_level         = DEBUG
        )

        return splash_screen

#### EOF ######################################################################


