# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Envisage GUI Application
------------------------

This class handles the life-cycle of a Pyface GUI.  Plugins can
display windows via mechinisms such as edit_traits().

This is intended to be a very simple shell for lifting an existing
pure TraitsUI or Pyface (or even Qt) app into an Envisage app.

More sophisticated applications should use Tasks.

"""

from traits.api import Event, Instance, observe
from envisage.api import Application
from envisage.ui.ids import IGUI_PROTOCOL


class GUIApplication(Application):
    """ The entry point for an Envisage GUI application.

    This class handles the life-cycle of a Pyface GUI.  Plugins can
    display windows via mechinisms such as edit_traits().

    This is intended to be a very simple shell for lifting an existing
    pure TraitsUI or Pyface (or even Qt) app into an Envisage app.

    More sophisticated applications should use Tasks.

    """

    #### 'GUIApplication' interface #########################################

    #: The Pyface GUI for the application.
    gui = Instance(IGUI_PROTOCOL)

    #: The splash screen for the application. By default, there is no splash
    #: screen.
    splash_screen = Instance("pyface.i_splash_screen.ISplashScreen")

    #### Application lifecycle events #########################################

    #: Fired after the GUI event loop has been started.
    application_initialized = Event

    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    def run(self):
        """ Run the application.

        Returns
        -------
        bool
            Whether the application started successfully (i.e., without a
            veto).

        """
        # show the splash screen if provided
        if self.splash_screen is not None:
            self.splash_screen.open()

        started = self.start()
        if started:
            if self.gui is None:
                gui_services = self.get_services(IGUI_PROTOCOL)
                if gui_services:
                    self.gui = gui_services[0]
                else:
                    # fall-back if not provided by plugin
                    from pyface.api import GUI
                    self.gui = GUI()
            self.gui.set_trait_later(self, "application_initialized", self)

            # Start the GUI event loop.  The application will block here.
            self.gui.start_event_loop()

            self.gui = None

            # clean up plugins once event loop stops
            self.stop()

        return started

    #### Trait observers ######################################################

    @observe('application_initialized')
    def _close_splash_screen(self, event):
        """Once the app has started we don't need the splash screen any more.
        """
        if self.splash_screen is not None:
            self.splash_screen.close()
            self.splash_screen.destroy()
            self.splash_screen = None
