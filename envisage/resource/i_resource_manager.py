# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The resource manager interface. """


# Enthought library imports.
from traits.api import Instance, Interface

# Local imports.
from .i_resource_protocol import IResourceProtocol


class IResourceManager(Interface):
    """ The resource manager interface. """

    # The protocols used by the manager to resolve resource URLs.
    resource_protocols = Instance(IResourceProtocol)

    def file(self, url):
        """ Return a readable file-like object for the specified url.

        Raise a 'NoSuchResourceError' if the resource does not exist.

        e.g.::

          manager.file('pkgfile://acme.ui.workbench/preferences.ini')

        """

#### EOF ######################################################################
