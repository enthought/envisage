# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The default implementation of the 'IMessage' interface. """


# Local imports.
from acme.motd.i_message import IMessage

# Enthought library imports.
from traits.api import HasTraits, provides, Str


@provides(IMessage)
class Message(HasTraits):
    """The default implementation of the 'IMessage' interface."""

    # The author of the message.
    author = Str

    # The text of the message.
    text = Str
