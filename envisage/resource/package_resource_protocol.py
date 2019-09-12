# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A resource protocol for package resources. """


# Standard library imports.
import errno, pkg_resources

# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_resource_protocol import IResourceProtocol
from .no_such_resource_error import NoSuchResourceError


@provides(IResourceProtocol)
class PackageResourceProtocol(HasTraits):
    """ A resource protocol for package resources.

    This protocol uses 'pkg_resources' to find and access resources.

    An address for this protocol is a string in the form::

        'package/resource'

    e.g::

        'acme.ui.workbench/preferences.ini'


    """

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """ Return a readable file-like object for the specified address. """

        first_forward_slash = address.index('/')

        package       = address[:first_forward_slash]
        resource_name = address[first_forward_slash+1:]

        try:
            f = pkg_resources.resource_stream(package, resource_name)

        except IOError as e:
            if e.errno == errno.ENOENT:
                raise NoSuchResourceError(address)

            else:
                raise

        except ImportError:
            raise NoSuchResourceError(address)

        return f

#### EOF ######################################################################
