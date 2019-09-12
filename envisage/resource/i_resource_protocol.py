# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The interface for protocols that handle resource URLs. """


# Enthought library imports.
from traits.api import Interface


class IResourceProtocol(Interface):
    """ The interface for protocols that handle resource URLs. """

    def file(self, address):
        """ Return a readable file-like object for the specified address.

        Raise a 'NoSuchResourceError' if the resource does not exist.

        e.g.::

          protocol.file('acme.ui.workbench/preferences.ini')

        """

#### EOF ######################################################################
