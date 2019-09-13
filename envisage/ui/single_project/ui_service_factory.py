# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
The default UI service factory.

"""


# Enthought library imports.
from traits.api import HasTraits, Int, Str

# Local imports.
from .ui_service import UiService


class UIServiceFactory(HasTraits):
    """
    The default UI service factory.

    """

    # The name of the class that implements the factory.
    class_name = Str

    # The priority of this factory
    priority = Int

    ###########################################################################
    # 'UIServiceFactory' interface.
    ###########################################################################

    def create_ui_service(self, *args, **kw):
        """ Create the UI service. """

        return UiService(*args, **kw)


#### EOF ######################################################################
