""" The 'Message of the Day' plugin """


# Enthought library imports.
from enthought.envisage3.api import Plugin

# Local imports.
from acme.motd.api import ExtensibleMOTD


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin """

    #### 'IPlugin' interface ##################################################

    # fixme: We can't do this yet since there is a bug in traits that a
    # default initializer in a base class 'trumps' a specific value in a
    # derived class!
##     # The plugin's unique identifier.
##     id = 'acme.motd.plugin'
            
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Initializers #########################################################

    # fixme: See the trait comment.
    def _id_default(self):
        """ Initializer. """

        return 'acme.motd.plugin'

    #### Methods ##############################################################

    def start(self, application):
        """ Start the plugin. """

        # fixme: Lookup the service?
        motd = ExtensibleMOTD()

        # Get the message of the day...
        message = motd.motd()

        # ... and print it.
        print '\n"%s"\n\n- %s' % (message.text, message.author)
        
        return

#### EOF ######################################################################
