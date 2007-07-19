""" The Envisage Action plugin. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.envisage.api import Plugin


# Logging.
logger = logging.getLogger(__name__)


class ActionPlugin(Plugin):
    """ The Envisage Action plugin. """
    
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self, application):
        """ Start the plugin. """

        return

    def stop(self, application):
        """ Stop the plugin. """

        return

### EOF ######################################################################
