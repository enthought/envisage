#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
An action to rename a data.

"""


# Standard imports.
import logging

# Local imports
from data_plugin_action import DataPluginAction


# Create a logger for this module.
logger = logging.getLogger(__name__)


class RenameDataAction(DataPluginAction):
    """
    An action to rename a data.

    """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    #### public interface #####################################################

    def perform(self, event):
        """
        Perform this action.

        """

        logger.debug('Performing action [%s]', self)

        event.tree.edit_label(event.node)

        return

#### EOF #####################################################################
