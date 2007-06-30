""" The 'Message of the Day' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin

# Local imports.
from acme.motd.api import IMOTD, ExtensibleMOTD


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin """
            
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

        # This is a bit of overkill here, but this shows how we can register
        # the MOTD object as a service so that other plugins can use it if
        # they so wish.
        application.register_service(IMOTD, ExtensibleMOTD())
        
        # And this is how we could look the service up!
        motd = application.get_service(IMOTD)

        # Get the message of the day...
        message = motd.motd()

        # ... and print it.
        print '\n"%s"\n\n- %s' % (message.text, message.author)
        
        return

#### EOF ######################################################################
