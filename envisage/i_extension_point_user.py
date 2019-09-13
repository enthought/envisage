# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The interface for objects using the 'ExtensionPoint' trait type. """


# Enthought library imports.
from traits.api import Instance, Interface

# Local imports.
from .i_extension_registry import IExtensionRegistry


class IExtensionPointUser(Interface):
    """ The interface for objects using the 'ExtensionPoint' trait type. """

    # The extension registry that the object's extension points are stored in.
    extension_registry = Instance(IExtensionRegistry)

#### EOF ######################################################################
