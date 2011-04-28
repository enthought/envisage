""" The 'Message of the Day' interface. """


# Enthought library imports.
from traits.api import Interface


class IMOTD(Interface):
    """ The 'Message of the Day' interface. """

    def motd(self):
        """ Return the message of the day.

        Returns an object that implements the 'IMessage' interface.

        """

#### EOF ######################################################################
