#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
A base class for actions that use the data plugin's services.

"""


# Standard library imports.
import logging

# Enthought library imports.
from envisage.api import UOL
from envisage.single_project.api import ProjectAction

# Data library imports.
from data.data import Data

# Application imports.
from data.plugin.services import IDATA_MODEL, IDATA_UI


# Create a logger for this module.
logger = logging.getLogger(__name__)


class DataPluginAction(ProjectAction):
    """
    A base class for actions that use the data plugin's services.

    """

    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'DataPluginAction' interface #################################

    # A reference to the data plugin's model service.
    data_model_service = UOL

    # A reference to the data plugin's UI service.
    data_ui_service = UOL


    ##########################################################################
    # 'object' interface
    ##########################################################################

    #### operator methods ####################################################

    def __init__(self, **kws):
        """
        Constructor.

        Extended to ensure that our UOL's have default identification strings.

        """

        super(DataPluginAction, self).__init__(**kws)

        if self.data_model_service is None:
            self.data_model_service = 'service://%s' % IDATA_MODEL

        if self.data_ui_service is None:
            self.data_ui_service = 'service://%s' % IDATA_UI

        return


    ##########################################################################
    # 'DataPluginAction' interface.
    ##########################################################################

    #### protected methods ###################################################

    def _get_target_data(self, event, show_error=True):
        """
        Return the data this action should import into.

        If the show_error parameter is True, then an error message will be
        displayed to the user if a data could not be located.

        """

        data = None

        # If the event has a node, then try to find the data from that node.
        if hasattr(event, 'node'):
            data = self._get_target_data_from_node(event.node)

        # If we don't have a data yet, then try and find it from the current
        # project selection.
        if data is None:
            data = self._get_target_data_from_project_selection()

        # If we have not identified a data, and we're supposed to show an error,
        # then do so now.
        if data is None and show_error:
            self._display_error('Unable to identify a Data to perform this '
                'action with.   Please select a target Data within the project '
                'tree and try again.')

        logger.debug('Target data: %s', data)

        return data


    def _get_target_data_from_node(self, node):
        """
        Locate the data this action should import into from the specified node.

        """

        # If the object itself is a data, then we're done
        obj = node.obj
        if isinstance(obj, Data):
            return obj

        # Otherwise, scan upward through the tree containing the node, looking
        # for the closest parent that is a data.
        data = None
        context = node.context
        while context is not None:
            if hasattr(context, 'adaptee'):
                obj = context.adaptee
                if isinstance(obj, Data):
                    data = obj
                    break
            if hasattr(context, 'context'):
                context = context.context
            else:
                context = None

        return data


    def _get_target_data_from_project_selection(self):
        """
        Locate the data this action should import into from project selection.

        """

        data = None

        # Find the first data in the project selection.
        for item in self.model_service.selection:
            if isinstance(item, Data):
                data = item
                break
            elif hasattr(item, 'obj') and isinstance(item.obj, Data):
                data = item.obj
                break

        return data

    def _get_node_name(self, event, show_error=True):
        """ Return the name of the selection
        """

        if hasattr(event, 'node'):
            if hasattr(event.node, 'name'):
                return event.node.name

        if show_error:
            logger.error('Could not retrieve the name of the selected data')

        return None
#### EOF #####################################################################

