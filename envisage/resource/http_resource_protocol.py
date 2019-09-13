# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A resource protocol for HTTP documents. """

# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_resource_protocol import IResourceProtocol
from .no_such_resource_error import NoSuchResourceError


@provides(IResourceProtocol)
class HTTPResourceProtocol(HasTraits):
    """ A resource protocol for HTTP documents. """

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        # Do the import here 'cos I'm not sure how much this will actually
        # be used.
        from .._compat import urlopen, HTTPError

        try:
            f = urlopen('http://' + address)

        except HTTPError:
            raise NoSuchResourceError('http:://' + address)

        return f

#### EOF ######################################################################
