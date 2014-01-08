""" The default implementation of the 'IMessage' interface. """


# Enthought library imports.
from traits.api import HasTraits, Str, provides

# Local imports.
from i_message import IMessage


@provides(IMessage)
class Message(HasTraits):
    """ The default implementation of the 'IMessage' interface. """

    # The author of the message.
    author = Str

    # The text of the message.
    text = Str

#### EOF ######################################################################
