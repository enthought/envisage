# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A test class used in the service registry tests! """


# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_foo import IFoo


@provides(IFoo)
class Foo(HasTraits):
    pass


#### EOF ######################################################################
