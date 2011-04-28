""" The Lorenz plugin. """


# Enthought library imports.
from envisage.api import Plugin, ServiceOffer
from traits.api import List


class LorenzPlugin(Plugin):
    """ The Lorenz plugin.

    This plugin is part of the 'Lorenz' example application.

    """

    # Extension points Ids.
    SERVICE_OFFERS = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.lorenz'

    # The plugin's name (suitable for displaying to the user).
    name = 'Lorenz'

    #### Contributions to extension points made by this plugin ################

    # Service offers.
    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        """ Trait initializer. """

        lorenz_service_offer = ServiceOffer(
            protocol = 'acme.lorenz.lorenz.Lorenz',
            factory  = 'acme.lorenz.lorenz.Lorenz'
        )

        return [lorenz_service_offer]

#### EOF ######################################################################
