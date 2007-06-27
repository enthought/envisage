""" The 'Message of the Day' plugin """


# Enthought library imports.
from enthought.envisage3.api import Plugin
from enthought.traits.api import Bool


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin """
    
    ###########################################################################
    # 'MOTD' interface.
    ###########################################################################

    #### 'MOTDPlugin' interface ###############################################

    started = Bool(False)
    stopped = Bool(False)
            
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Initializer. """

        return 'acme.motd.plugin'

    #### Methods ##############################################################
    
    def start(self, application):
        """ Start the plugin. """
        
        self.started = True
        self.stopped = False
        
        return

    def stop(self, application):
        """ Stop the plugin. """
        
        self.started = False
        self.stopped = True
        
        return

#### EOF ######################################################################
