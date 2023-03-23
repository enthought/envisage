# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The 'Message of the Day' plugin """


# In the interest of lazy loading you should only import from the following
# packages at the module level of a plugin::
#
# - envisage
# - traits
#
# Eveything else should be imported when it is actually required.


from traits.api import Instance, List, on_trait_change

# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin, ServiceOffer


class MOTDPlugin(Plugin):
    """The 'Message of the Day' plugin.

    This plugin simply prints the 'Message of the Day' to stdout.

    """

    # The Ids of the extension points that this plugin offers.
    MESSAGES = "acme.motd.messages"

    # The Ids of the extension points that this plugin contributes to.
    SERVICE_OFFERS = "envisage.service_offers"

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = "acme.motd"

    # The plugin's name (suitable for displaying to the user).
    name = "MOTD"

    #### Extension points offered by this plugin ##############################

    # The messages extension point.
    #
    # Notice that we use the string name of the 'IMessage' interface rather
    # than actually importing it. This makes sure that the import only happens
    # when somebody actually gets the contributions to the extension point.
    messages = ExtensionPoint(
        List(Instance("acme.motd.api.IMessage")),
        id=MESSAGES,
        desc="""

        This extension point allows you to contribute messages to the 'Message
        Of The Day'.

        """,
    )

    #### Contributions to extension points made by this plugin ################

    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        """Trait initializer."""

        # Register the protocol as a string containing the actual module path
        # and *not* a module path that goes via an 'api.py' file as this does
        # not match what Python thinks the module is! This allows the service
        # to be looked up by passing either the exact same string, or the
        # actual protocol object itself (the latter is the preferred way of
        # doing it!).
        motd_service_offer = ServiceOffer(
            protocol="acme.motd.i_motd.IMOTD",
            factory=self._create_motd_service,
        )

        return [motd_service_offer]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_motd_service(self):
        """Factory method for the 'MOTD' service."""

        # Only do imports when you need to! This makes sure that the import
        # only happens when somebody needs an 'IMOTD' service.
        from acme.motd.motd import MOTD

        return MOTD(messages=self.messages)

    # This plugin does all of its work in this method which gets called when
    # the application has started all of its plugins.
    @on_trait_change("application:started")
    def _print_motd(self):
        """Print the 'Message of the Day' to stdout!"""

        # Note that we always offer the service via its name, but look it up
        # via the actual protocol.
        from acme.motd.api import IMOTD

        # Lookup the MOTD service.
        motd = self.application.get_service(IMOTD)

        # Get the message of the day...
        message = motd.motd()

        # ... and print it.
        print('\n"%s"\n\n- %s' % (message.text, message.author))
