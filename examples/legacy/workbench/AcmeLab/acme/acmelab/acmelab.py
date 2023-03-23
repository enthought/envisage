# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Acme Lab application. """


# Standard library imports.
from logging import DEBUG

# Enthought library imports.
from envisage.ui.workbench.api import WorkbenchApplication
from pyface.api import AboutDialog, ImageResource, SplashScreen


class Acmelab(WorkbenchApplication):
    """ The Acme Lab application. """

    #### 'IApplication' interface #############################################

    # The application's globally unique Id.
    id = "acme.acmelab"

    #### 'WorkbenchApplication' interface #####################################

    # Branding information.
    #
    # The icon used on window title bars etc.
    icon = ImageResource("acmelab.ico")

    # The name of the application (also used on window title bars etc).
    name = "Acme Lab"

    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    def _about_dialog_default(self):
        """ Trait initializer. """

        about_dialog = AboutDialog(
            parent=self.workbench.active_window.control,
            image=ImageResource("about"),
        )

        return about_dialog

    def _splash_screen_default(self):
        """ Trait initializer. """

        splash_screen = SplashScreen(
            image=ImageResource("splash"),
            show_log_messages=True,
            log_level=DEBUG,
        )

        return splash_screen
