""" The default implementation of the 'IPlugin' interface. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import HasTraits, Str, implements

# Local imports.
from i_plugin import IPlugin


# Logging.
logger = logging.getLogger(__name__)


class Plugin(HasTraits):
    """ The default implementation of the 'IPlugin' interface. """

    implements(IPlugin)

    #### 'IPlugin' interface ##################################################
    
    # The plugin's unique identifier.
    id = Str

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Initializers #########################################################
    
    def _id_default(self):
        """ Initializer. """

        return '%s.%s' % (type(self).__module__, type(self).__name__)
    
    #### Methods ##############################################################
 
    def start(self, plugin_context):
        """ Start the plugin. """

        pass

    def stop(self, plugin_context):
        """ Stop the plugin. """

        pass

#### EOF ######################################################################
