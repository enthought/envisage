""" The 'Message of the Day' implementation! """


# Standard library imports.
from random import choice

# Enthought library imports.
from enthought.traits.api import HasTraits, List

# Local imports.
from i_message import IMessage
from message import Message


class MOTD(HasTraits):
    """ The 'Message of the Day' implementation! """

    DEFAULT_MESSAGE = Message(
        author='Anon', text='Work hard and be good to your Mother'
    )

    # The list of possible messages.
    messages = List(IMessage)

    ###########################################################################
    # 'MOTD' interface.
    ###########################################################################

    def motd(self):
        """ Prints a random message. """

        if len(self.messages) > 0:
            message = choice(self.messages)

        else:
            message = self.DEFAULT_MESSAGE

        return message
    
#### EOF ######################################################################
