# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The 'Software Quotes' plugin """


from traits.api import List

# Enthought library imports.
from envisage.api import Plugin


class SoftwareQuotesPlugin(Plugin):
    """The 'Software Quotes' plugin."""

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = "acme.motd.software_quotes"

    # The plugin's name (suitable for displaying to the user).
    name = "Software Quotes"

    #### Extension points offered by this plugin ##############################

    # None

    #### Contributions to extension points made by this plugin ################

    # Messages for the 'Message Of The Day'.
    messages = List(contributes_to="acme.motd.messages")

    def _messages_default(self):
        """Trait initializer."""

        # Only do imports when you need to!
        from acme.motd.software_quotes.messages import messages

        return messages
