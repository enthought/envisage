""" The 'Message of the Day' plugin """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin
from enthought.traits.api import List

# Local imports.
from i_message import IMessage
from i_motd import IMOTD
from motd import MOTD


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin """

    #### 'IPlugin' interface ##################################################

    id          = 'acme.motd'
    name        = 'MOTD'
    description = 'The ACME Message of the Day (MOTD) Plugin'
    requires    = []

    #### Extension points #####################################################

    # The messages extension point.
    messages = ExtensionPoint(
        List(IMessage), id='acme.motd.messages', desc = """

        This extension point allows you to contribute messages to the 'Message
        Of The Day'.

        """
    )
    
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # Use the contributed messages to create a MOTD object.
        motd = MOTD(messages=self.messages)
        
        # Publish the object as a service.
        #
        # This is a bit of overkill here, but this shows how we can register
        # the MOTD object as a service so that other parts of the application
        # can use it if they so wish (it just so happens that this application
        # is so small, that there aren't any other parts')!
        self._motd_service_id = self.application.register_service(IMOTD, motd)
        
        # And this is how we could look the service up!
        motd_service = self.application.get_service(IMOTD)

        # Get the message of the day...
        message = motd_service.motd()

        # ... and print it.
        print '\n"%s"\n\n- %s' % (message.text, message.author)
        
        return

    def stop(self):
        """ Stop the plugin. """

        # Unregister the MOTD service.
        self.application.unregister_service(self._motd_service_id)
        
        return

#### EOF ######################################################################
