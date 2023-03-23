# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The 'Message of the Day' interface. """


# Enthought library imports.
from traits.api import Interface


class IMOTD(Interface):
    """The 'Message of the Day' interface."""

    def motd(self):
        """Return the message of the day.

        Returns an object that implements the 'IMessage' interface.

        """
