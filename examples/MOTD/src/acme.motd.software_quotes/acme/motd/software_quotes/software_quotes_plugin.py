""" The 'Software Quotes' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin, extension_point


class SoftwareQuotesPlugin(Plugin):
    """ The 'Software Quotes' plugin """

    PREFERENCES = 'pkgfile://acme.motd.software_quotes/preferences.ini'
    
    #### 'IPlugin' interface ##################################################

    id          = 'acme.motd.software_quotes'
    name        = 'Software Quotes'
    description = 'The Software Quotes Plugin'
    requires    = []
    
    ###########################################################################
    # Extension point contributions.
    ###########################################################################

    @extension_point('enthought.envisage.preferences')
    def enthought_envisage_preferences(self, application):
        """ Extension point contribution. """

        return [SoftwareQuotesPlugin.PREFERENCES]

    @extension_point('acme.motd.messages')
    def get_messages(self, application):
        """ Extension point contribution. """

        from messages import messages

        return messages

#### EOF ######################################################################
