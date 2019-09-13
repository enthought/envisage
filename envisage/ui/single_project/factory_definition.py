# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#Enthought imports
from traits.api import HasTraits, Int, Str

class FactoryDefinition(HasTraits):
    """
    A project factory definition.

    An instance of the specified class is used to open and/or create new
    projects.

    The extension with the highest priority wins!  In the event of a tie,
    the first instance wins.

    """

    # The name of the class that implements the factory.
    class_name = Str

    # The priority of this factory
    priority = Int
