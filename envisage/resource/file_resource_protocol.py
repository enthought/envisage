# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A resource protocol for a local file system. """


# Standard library imports.
import errno

# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_resource_protocol import IResourceProtocol
from .no_such_resource_error import NoSuchResourceError


@provides(IResourceProtocol)
class FileResourceProtocol(HasTraits):
    """ A resource protocol for a local file system. """

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        # Opened in binary mode to be consistent with package resources. This
        # means, for example, that line-endings will not be converted.
        try:
            f = open(address, 'rb')

        except IOError as e:
            if e.errno == errno.ENOENT:
                raise NoSuchResourceError(address)

            else:
                raise

        return f

#### EOF ######################################################################
