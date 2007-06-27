""" The 'Foo' plugin """


# Enthought library imports.
from enthought.envisage3.api import Plugin
from enthought.traits.api import Bool


class FooPlugin(Plugin):
    """ The 'Foo' plugin """
    
    #### 'FooPlugin' interface ################################################

    started = Bool(False)
    stopped = Bool(False)
            
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Initializer. """

        return 'acme.foo'

    #### Methods ##############################################################
    
    def start(self, plugin_context):
        """ Start the plugin. """
        
        self.started = True
        self.stopped = False
        
        return

    def stop(self, plugin_context):
        """ Stop the plugin. """
        
        self.started = False
        self.stopped = True
        
        return

#### EOF ######################################################################
