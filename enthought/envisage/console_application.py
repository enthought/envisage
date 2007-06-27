""" The entry point for an Envisage Console application. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.envisage3.api import Application


# Logging.
logger = logging.getLogger(__name__)


class ConsoleApplication(Application):
    """ The entry point for an Envisage Console application.

    i.e. a command line application.

    """

    ###########################################################################
    # 'ConsoleApplication' interface.
    ###########################################################################

    #### Methods ##############################################################

    def run(self):
        """ Runs the application.

        This does the following (so you don't have to ;^):-

        1) Starts the application
        2) Stops the application

        """

        logger.debug('---------- console application ----------')

        # Start the application.
        self.start()

        # Stop the application to give all of the plugins a chance to close
        # down cleanly and to do any housekeeping etc.
        self.stop()
        
        return
        
#### EOF ######################################################################
