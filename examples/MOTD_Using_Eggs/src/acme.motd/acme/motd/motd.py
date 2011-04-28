""" The 'Message of the Day' implementation! """


# Standard library imports.
from random import choice

# Enthought library imports.
from traits.api import HasTraits, List, implements

# Local imports.
from i_message import IMessage
from i_motd import IMOTD
from message import Message


class MOTD(HasTraits):
    """ The 'Message of the Day' implementation! """

    implements(IMOTD)

    # The default message is used when there are no other messages!
    DEFAULT_MESSAGE = Message(
        author='Anon', text='Work hard and be good to your Mother'
    )

    # The list of possible messages.
    messages = List(IMessage)

    ###########################################################################
    # 'IMOTD' interface.
    ###########################################################################

    def motd(self):
        """ Prints a random message. """

        if len(self.messages) > 0:
            message = choice(self.messages)

        else:
            message = self.DEFAULT_MESSAGE

        return message

#### EOF ######################################################################
