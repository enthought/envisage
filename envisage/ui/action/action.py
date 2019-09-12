# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The *definition* of an action in a tool bar or menu. """


# Enthought library imports.
from traits.api import Str

# Local imports.
from .location import Location


class Action(Location):
    """ The *definition* of an action in a tool bar or menu. """

    #### Action implementation ################################################

    # The action's name (appears on menus and toolbars etc).
    name = Str

    # The name of the class that implements the action.
    class_name = Str

    ###########################################################################
    # 'object' interface
    ###########################################################################

    def __str__(self):
        """ Return the 'informal' string representation of the object. """

        return 'Action(%s)' % self.name

    __repr__ = __str__

#### EOF ######################################################################
