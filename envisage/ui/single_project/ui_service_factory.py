#-----------------------------------------------------------------------------
#
#  Copyright (c) 2006-2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

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
