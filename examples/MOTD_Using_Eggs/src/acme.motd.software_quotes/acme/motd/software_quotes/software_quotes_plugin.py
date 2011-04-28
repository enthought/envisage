""" The 'Software Quotes' plugin """


# Enthought library imports.
from envisage.api import Plugin
from traits.api import List


class SoftwareQuotesPlugin(Plugin):
    """ The 'Software Quotes' plugin. """

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.motd.software_quotes'

    # The plugin's name (suitable for displaying to the user).
    name = 'Software Quotes'

    #### Extension points offered by this plugin ##############################

    # None

    #### Contributions to extension points made by this plugin ################

    # Messages for the 'Message Of The Day'.
    messages = List(contributes_to='acme.motd.messages')

    def _messages_default(self):
        """ Trait initializer. """

        # Only do imports when you need to!
        from messages import messages

        return messages

#### EOF ######################################################################
