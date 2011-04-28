#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
An action set for contributing actions to Data.

"""

# Enthought library imports.
from envisage.action.action_plugin_definition import ActionSet


##############################################################################
# Constants
##############################################################################

# A commonly used string within our declarations.
ROOT = 'data.plugin.resource_type'

# The prefix used to identify menu-building resources, within an action set,
# for the context menu applying to a Data.  This string MUST MATCH the string
# that the Data's node type is looking for!
DATA_CONTEXT_MENU = '%s.data_node_type' % ROOT


class DataActionSet(ActionSet):
    """
    Action and menu definitions for the project view.

    """

    # A mapping from human-readable root names to globally unique Ids.
    aliases = {
        'DataContextMenu': DATA_CONTEXT_MENU
        }


#### EOF #####################################################################

