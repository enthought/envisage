""" The default implementation of the 'IPlugin' interface. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import HasTraits, List, Str, implements

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

    # The plugin's name (suitable for displaying to the user).
    name = Str

    # A description of what the plugin is and does.
    description = Str

    # The Ids of the plugins that must be started before this one is started
    # (this is usually because this plugin requires a service that the other
    # plugin starts).
    requires = List(Str)
    
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Initializers #########################################################

    # fixme: Traits bug... this trumps any explicit 'id = ...' in subclasses!
##     def _id_default(self):
##         """ Initializer. """

##         return '%s.%s' % (type(self).__module__, type(self).__name__)
    
    #### Methods ##############################################################
 
    def start(self, plugin_context):
        """ Start the plugin. """

        pass

    def stop(self, plugin_context):
        """ Stop the plugin. """

        pass

#### EOF ######################################################################
