""" The 'Software Quotes' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin, extension_point
from enthought.traits.api import Str

# Acme imports.
from acme.motd.api import IMessage


class SoftwareQuotesPlugin(Plugin):
    """ The 'Software Quotes' plugin """

    PREFS = 'pkgfile://acme.motd.software_quotes/preferences.ini'
    
    #### 'IPlugin' interface ##################################################

    id          = 'acme.motd.software_quotes'
    name        = 'Software Quotes'
    description = 'The Software Quotes Plugin'
    requires    = []

    #### Contributions to extension points ####################################

    # This shows how traits can be used to make contributions...
    preferences = Str(PREFS, extension_point='enthought.envisage.preferences')
    
    ###########################################################################
    # Contributions to extension points.
    ###########################################################################

    # These show how methods can be used to make contributions through either
    #
    # a) a method with the same name as the extension point Id..
    def enthought_envisage_preferences(self, application):
        """ Extension point contribution. """

        return 'pkgfile://acme.motd.software_quotes/preferences.ini'

    # b) an explicit decorator...
    @extension_point('acme.motd.messages')
    def get_messages(self, application):
        """ Extension point contribution. """

        from messages import messages

        return messages

#### EOF ######################################################################
