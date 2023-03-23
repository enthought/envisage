# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The 'Message of the Day' implementation! """


# Standard library imports.
from random import choice

# Local imports.
from acme.motd.i_message import IMessage
from acme.motd.i_motd import IMOTD
from acme.motd.message import Message

# Enthought library imports.
from traits.api import HasTraits, List, provides


@provides(IMOTD)
class MOTD(HasTraits):
    """The 'Message of the Day' implementation!"""

    # The default message is used when there are no other messages!
    DEFAULT_MESSAGE = Message(
        author="Anon", text="Work hard and be good to your Mother"
    )

    # The list of possible messages.
    messages = List(IMessage)

    ###########################################################################
    # 'IMOTD' interface.
    ###########################################################################

    def motd(self):
        """Prints a random message."""

        if len(self.messages) > 0:
            message = choice(self.messages)

        else:
            message = self.DEFAULT_MESSAGE

        return message
