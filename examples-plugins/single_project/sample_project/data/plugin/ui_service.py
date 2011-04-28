#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
The UI service for the Data plugin.

"""

# Standard library imports.
import logging

# Enthought library imports.
from envisage.api import ApplicationObject, UOL
from pyface.api import confirm, error, FileDialog, information, YES

# Data library imports.

# Local imports.
from services import IDATA_MODEL


# Setup a logger for this module
logger = logging.getLogger(__name__)


class UiService(ApplicationObject):
    """
    The UI service for the Data plugin.

    """

    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'UiService' interface ########################################

    # A reference to the Data plugin's model service.
    model_service = UOL


    ##########################################################################
    # 'Object' interface
    ##########################################################################

    #### operator methods ####################################################

    def __init__(self, **kws):
        """
        Constructor.

        Extended to ensure our UOL properties are set.

        """

        super(UiService, self).__init__(**kws)

        # Ensure we have a default model-service if one wasn't specified.
        if self.model_service is None:
            self.model_service = 'service://%s' % IDATA_MODEL

        return


    ##########################################################################
    # 'UIService' interface
    ##########################################################################

    #### public methods ######################################################



    #TODO cgalvan: to be implemented
#    def delete_data(self, context, data_name, parent_window):
#        """
#        Delete a Data.
#
#        """
#
#        # Open confirmation-dialog to confirm deletion
#        message = 'Are you sure you want to delete %s?' % data_name
#        if confirm(parent_window, message) == YES:
#            self.model_service.delete_context_item(context, data_name)
#
#        return

    def edit_data(self, window, data):
        """
        Edit the data parameters of the specified data.

        """

        data_parameters = data.data_parameters

        edit_ui = data_parameters.edit_traits(view='data_view',
                                              kind = 'livemodal',
                                              # handler=handler,
                                              parent=window)

        return edit_ui.result

    def display_message(self, msg, title=None, is_error=False):
        """
        Display the specified message to the user.

        """

        # Ensure we record any reasons this method doesn't work.  Especially
        # since it's critical in displaying errors to users!
        try:

            # Attempt to identify the current application window.
            parent_window = None
            workbench = self.application.get_service('envisage.'
                'workbench.IWorkbench')
            if workbench is not None:
                parent_window = workbench.active_window.control

            # Display the requested message
            if is_error:
                error(parent_window, msg, title=title)
            else:
                information(parent_window, msg, title=title)

        except:
            logger.exception('Unable to display pop-up message')

        return

#### EOF #####################################################################

