""" The interface for 'Message of the Day' messages. """


# Enthought library imports.
from traits.api import Interface, Str


class IMessage(Interface):
    """ The interface for 'Message of the Day' messages. """

    # The author of the message.
    author = Str

    # The text of the message.
    text = Str

#### EOF ######################################################################
