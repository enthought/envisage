""" The 'Software Quotes' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class SoftwareQuotesPlugin(Plugin):
    """ The 'Software Quotes' plugin. """

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.motd.software_quotes'

    # The plugin's name (suitable for displaying to the user).
    name = 'Software Quotes'

    #### Extension point contributions ########################################

    # Messages for the 'Message Of The Day'.
    messages = List(extension_point='acme.motd.messages')
    
    ###########################################################################
    # 'SoftwareQuotesPlugin' interface.
    ###########################################################################

    def _messages_default(self):
        """ Trait initializer. """

        # Only do imports when you need to!
        from messages import messages

        return messages

#### EOF ######################################################################
