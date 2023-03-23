# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A resource protocol for package resources. """


# Standard library imports.
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_resource_protocol import IResourceProtocol
from .no_such_resource_error import NoSuchResourceError


@provides(IResourceProtocol)
class PackageResourceProtocol(HasTraits):
    """A resource protocol for package resources.

    This protocol uses 'importlib.resources' to find and access resources.

    An address for this protocol is a string in the form::

        'package/resource'

    e.g::

        'acme.ui.workbench/preferences.ini'
    """

    ###########################################################################
    # 'IResourceProtocol' interface.
    ###########################################################################

    def file(self, address):
        """Return a readable file-like object for the specified address."""

        package, *resource_path = address.split("/")

        if not package or not resource_path:
            raise NoSuchResourceError(address)

        try:
            f = files(package).joinpath(*resource_path).open("rb")
        except (
            ModuleNotFoundError,
            TypeError,  # TypeError is raised if package is a module
            FileNotFoundError,
            IsADirectoryError,
            PermissionError,
        ):
            raise NoSuchResourceError(address)

        return f
