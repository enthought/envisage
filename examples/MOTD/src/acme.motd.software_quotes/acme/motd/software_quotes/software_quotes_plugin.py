""" The 'Software Quotes' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin, extension


class SoftwareQuotesPlugin(Plugin):
    """ The 'Software Quotes' plugin """

    #### 'IPlugin' interface ##################################################

    id          = 'acme.motd.software_quotes'
    name        = 'Software Quotes'
    description = 'The Software Quotes Plugin'
    requires    = []

    ###########################################################################
    # Extension point contributions.
    ###########################################################################

    @extension('enthought.envisage.preferences')
    def enthough_envisage_preferences(self, application):
        """ Extension point contribution. """

        return 'pkgfile://acme.motd.software_quotes/preferences.ini'

    @extension('acme.motd.messages')
    def acme_motd_messages(self, application):
        """ Extension point contribution. """

        from messages import messages

        return messages

#### EOF ######################################################################
