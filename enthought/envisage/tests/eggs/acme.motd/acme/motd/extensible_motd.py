""" An extensible MOTD class. """


# Enthought library imports.
from enthought.envisage3.api import ExtensionPoint
from enthought.traits.api import List

# Local imports.
from i_message import IMessage
from motd import MOTD


class ExtensibleMOTD(MOTD):
    """ An extensible MOTD class. """

    messages = ExtensionPoint(List(IMessage), id='acme.motd.messages')

#### EOF ######################################################################
