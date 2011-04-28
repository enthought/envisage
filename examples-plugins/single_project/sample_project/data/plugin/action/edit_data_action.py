#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
An action to edit the data parameters of a Data.

"""


# Standard imports.
import logging

# Local imports
from data_plugin_action import DataPluginAction


# Create a logger for this module.
logger = logging.getLogger(__name__)


class EditDataAction(DataPluginAction):
    """
    An action to edit the data parameters of a data.

    """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    #### public interface #####################################################

    def perform(self, event):
        """
        Perform this action.

        """

        logger.debug('Performing EditDataAction [%s]', self)

        # Pull the parent for any displayed UI from the event.
        window = event.window.control

        # If we can find a target data, then perform the operation.
        data = self._get_target_data(event)
        if data is not None:
            self.data_ui_service.edit_data(window, data)

        return


#### EOF #####################################################################
