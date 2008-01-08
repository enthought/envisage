""" The entry point for an Envisage Workbench application. """


# Standard library imports.
import logging

# Enthought library imports.
#
# fixme: The ordering of these imports is critical. We don't use traits UI in
# this module, but it must be imported *before* any 'HasTraits' class whose
# instances might want to have 'edit_traits' called on them.
#
# fixme: Just importing the package is enought (see above).
import enthought.traits.ui

# Enthought library imports.
from enthought.envisage.api import Application
from enthought.pyface.api import AboutDialog, Dialog, GUI, ImageResource
from enthought.pyface.api import SplashScreen
from enthought.pyface.workbench.api import IWorkbench
from enthought.traits.api import Callable, Instance, Str, Tuple

# Local imports.
from workbench import Workbench


# Logging.
logger = logging.getLogger(__name__)


class WorkbenchApplication(Application):
    """ The entry point for an Envisage Workbench application.

    i.e. a GUI application whose user interface is provided by the workbench
    plugin.

    """

    #### 'WorkbenchApplication' interface #####################################

    # The PyFace GUI for the application (this is here to make it easy for
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
    icon = Instance(ImageResource, ImageResource('application.ico'))
    
    # The name of the application (also used on window title bars etc).
    name = Str('Workbench')
    
    # The splash screen (None, the default, if no splash screen is required).
    splash_screen = Instance(SplashScreen)

    # The default position of the main window.
    window_position = Tuple((200, 200))
    
    # The default size of the main window.
    window_size = Tuple((800, 600))
    
    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _about_dialog_default(self):
        """ Trait initializer. """

        about_dialog = AboutDialog(
            parent = self.workbench.active_window.control,
            image  = ImageResource('about')
        )

        return about_dialog
    
    def _gui_default(self):
        """ Trait initializer. """

        return GUI(splash_screen=self.splash_screen)

    def _workbench_default(self):
        """ Trait initializer. """

        return self.create_workbench()
    
    #### Methods ##############################################################

    def create_workbench(self):
        """ Create the workbench. """

        logger.debug('workbench factory %s', self.workbench_factory)

        return self.workbench_factory(application=self)

    def run(self):
        """ Run the application.

        This does the following (so you don't have to ;^):-

        1) Starts the application
        2) Creates and opens a workbench window.
        3) Starts the GUI event loop
        4) When the event loop terminates, stops the application

        """

        logger.debug('---------- workbench application ----------')

        # Make sure the GUI has been created (so that, if required, the splash
        # screen is shown).
        gui = self.gui
        
        # Start the application.
        self.start()

        # Create and open the first workbench window.
        window = self.workbench.create_window(
            position=self.window_position, size=self.window_size
        )
        window.open()

        # Start the GUI event loop.
        #
        # THIS CALL DOES NOT RETURN UNTIL THE GUI IS CLOSED.
        gui.start_event_loop()

        # Stop the application.
        self.stop()
        
        return
        
#### EOF ######################################################################
