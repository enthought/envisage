""" The developer plugin. """


# Enthought library imports.
from envisage.api import Plugin, ServiceOffer
from traits.api import List


# The package that this module is in.
PKG = '.'.join(__name__.split('.')[:-1])


class DeveloperPlugin(Plugin):
    """ The developer plugin.

    This plugin contains the non-GUI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    # The Ids of the extension points that this plugin contributes to.
    SERVICE_OFFERS = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's globally unique identifier.
    id = 'envisage.developer'

    # The plugin's name (suitable for displaying to the user).
    name = 'Developer'

    #### Extension points offered by this plugin ##############################

    # None.

    #### Contributions to extension points made by this plugin ################

    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        """ Trait initializer. """

        code_browser_class = PKG + '.code_browser.api.CodeBrowser'

        code_browser_service_offer = ServiceOffer(
            protocol = code_browser_class,
            factory  = code_browser_class,
            scope    = 'application'
        )

        return [code_browser_service_offer]

#### EOF ######################################################################
