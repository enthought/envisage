""" The 'Message of the Day' plugin """


# In the interest of lazy loading you should only import from the following
# packages at the module level of a plugin::
#
# - enthought.envisage
# - enthought.traits
#
# Eveything else should be imported when it is actually required.


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin, ServiceOffer
from enthought.traits.api import Instance, List


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin.

    When this plugin is started it prints the 'Message of the Day' to stdout.
    
    """

    # The Ids of the extension points that this plugin offers.
    MESSAGES = 'acme.motd.messages'

    # The Ids of the extension points that this plugin contributes to.
    SERVICE_OFFERS = 'enthought.envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.motd'

    # The plugin's name (suitable for displaying to the user).
    name = 'MOTD'

    #### Extension points offered by this plugin ##############################

    # The messages extension point.
    #
    # Notice that we use the string name of the 'IMessage' interface rather
    # than actually importing it. This makes sure that the import only happens
    # when somebody actually gets the contributions to the extension point.
    messages = ExtensionPoint(
        List(Instance('acme.motd.api.IMessage')), id=MESSAGES, desc = """

        This extension point allows you to contribute messages to the 'Message
        Of The Day'.

        """
    )

    #### Contributions to extension points made by this plugin ################

    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        """ Trait initializer. """
        
        motd_service_offer = ServiceOffer(
            protocol='acme.motd.api.IMOTD', factory=self._motd_factory,
        )

        return [motd_service_offer]
    
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # Lookup the MOTD service.
        motd = self.application.get_service('acme.motd.api.IMOTD')

        # Get the message of the day...
        message = self.application.get_service('acme.motd.api.IMOTD').motd()

        # ... and print it.
        print '\n"%s"\n\n- %s' % (message.text, message.author)
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _motd_factory(self):
        """ Factory for the 'MOTD' service. """

        # Only do imports when you need to! This makes sure that the import
        # only happens when somebody needs an 'IMOTD' service.
        from motd import MOTD

        return MOTD(messages=self.messages)
    
#### EOF ######################################################################
