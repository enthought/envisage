""" The 'Software Quotes' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import List


class SoftwareQuotesPlugin(Plugin):
    """ The 'Software Quotes' plugin """

    #### 'IPlugin' interface ##################################################

    id          = 'acme.motd.software_quotes'
    name        = 'Software Quotes'
    description = 'The Software Quotes Plugin'
    requires    = []

    #### Extension point contributions ########################################

    messages    = List(extension_point='acme.motd.messages')
    
    ###########################################################################
    # 'SoftwareQuotesPlugin' interface.
    ###########################################################################

    def _messages_default(self):
        """ Trait initializer. """

        from messages import messages

        return messages

#### EOF ######################################################################
