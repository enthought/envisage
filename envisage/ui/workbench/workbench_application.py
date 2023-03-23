# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The entry point for an Envisage Workbench application. """


# Standard library imports.
import logging

from pyface.api import AboutDialog, Dialog, GUI, ImageResource, SplashScreen
from pyface.workbench.api import IWorkbench
from traits.api import Callable, Instance, Str, Tuple

# Enthought library imports.
from envisage.api import Application

# Local imports.
from .workbench import Workbench

# Logging.
logger = logging.getLogger(__name__)


class WorkbenchApplication(Application):
    """The entry point for an Envisage Workbench application.

    i.e. a GUI application whose user interface is provided by the workbench
    plugin.

    This class handles the common case for Workbench applications, and it is
    intended to be subclassed to change start/stop behaviour etc. In fact, I
    generally create a subclass for every Workbench application I write since
    it is a good place to put branding information etc.

    """

    #### 'WorkbenchApplication' interface #####################################

    # The Pyface GUI for the application (this is here to make it easy for
    # parts of the application to get a reference to the GUI so they can get
    # system metrics, etc.
    gui = Instance(GUI)

    # The workbench.
    workbench = Instance(IWorkbench)

    # The factory for creating the workbench (used *instead* of providing a
    # workbench explicitly).
    workbench_factory = Callable(Workbench)

    # Branding information.
    #
    # The 'About' dialog.
    about_dialog = Instance(Dialog)

    # The icon used on window title bars etc.
    icon = Instance(ImageResource, ImageResource("application.ico"))

    # The name of the application (also used on window title bars etc).
    name = Str("Workbench")

    # The splash screen (None, the default, if no splash screen is required).
    splash_screen = Instance(SplashScreen)

    # The default position of the main window.
    window_position = Tuple((200, 200))

    # The default size of the main window.
    window_size = Tuple((800, 600))

    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    def run(self):
        """Run the application.

        This does the following (so you don't have to ;^):-

        1) Starts the application
        2) Creates and opens a workbench window
        3) Starts the GUI event loop
        4) When the event loop terminates, stops the application

        """

        logger.debug("---------- workbench application ----------")

        # Make sure the GUI has been created (so that, if required, the splash
        # screen is shown).
        gui = self.gui

        # Start the application.
        if self.start():
            # Create and open the first workbench window.
            window = self.workbench.create_window(
                position=self.window_position, size=self.window_size
            )
            window.open()

            # We stop the application when the workbench has exited.
            self.workbench.on_trait_change(self._on_workbench_exited, "exited")

            # Start the GUI event loop.
            #
            # THIS CALL DOES NOT RETURN UNTIL THE GUI IS CLOSED.
            gui.start_event_loop()

    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _about_dialog_default(self):
        """Trait initializer."""

        return AboutDialog(image=ImageResource("about"))

    def _gui_default(self):
        """Trait initializer."""

        return GUI(splash_screen=self.splash_screen)

    def _workbench_default(self):
        """Trait initializer."""

        return self.create_workbench()

    #### Methods ##############################################################

    def about(self):
        """Display the about dialog."""

        # fixme: We really need to create a new 'about dialog' every time so
        # that it can have the active window as its parent.
        self.about_dialog.open()

    # fixme: Is this needed on the public API? Why can't we just do this in
    # the default initializer (_workbench_default)?
    def create_workbench(self):
        """Create the workbench."""

        logger.debug("workbench factory %s", self.workbench_factory)

        return self.workbench_factory(application=self)

    def exit(self):
        """Exit the application.

        This closes all open windows and hence exits the GUI event loop.

        """

        self.workbench.exit()

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _on_workbench_exited(self):
        """Dynamic trait change handler."""

        # We don't invoke 'stop' directly because:-
        #
        # The workbench is often exited via a user action (either by closing
        # the last open window, or by choosing 'File/Exit'). If this happens
        # then the workbench 'exit' method is called from within an event
        # handler which would cause the 'stop' method to get called *before*
        # the handling of the window 'closed' event is complete. Hance, this
        # might mean that somebody listening for the window being closed would
        # get the event *after* the application had already stopped!
        self.gui.invoke_later(self.stop)
