# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The *definition* of a group in a tool bar or menu. """


# Enthought library imports.
from traits.api import Bool, Str

# Local imports.
from .location import Location


class Group(Location):
    """ The *definition* of a group in a tool bar or menu. """

    # The group's unique identifier (unique within the tool bar, menu bar or
    # menu that the group is to be added to).
    id = Str

    # Does this group require a separator?
    separator = Bool(True)

    # The optional name of a class that implements the group. The class must
    # support the **pyface.action.Group** protocol.
    class_name = Str

    ###########################################################################
    # 'object' interface
    ###########################################################################

    def __str__(self):
        """ Return the 'informal' string representation of the object. """

        return 'Group(%s)' % self.id

    __repr__ = __str__

#### EOF ######################################################################
