#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
An action set for contributing actions to components of a env
project.

"""


# Enthought library imports.
from envisage.single_project.plugin_definition import \
    NO_SELECTION_MENU_ID, PROJECT_MENU_ID, SingleProjectActionSet


##############################################################################
# Constants
##############################################################################


# A commonly used string within our declarations.
ROOT = 'plugins.single_project.resource_type'


class EnvProjectActionSet(SingleProjectActionSet):
    """
    Action and menu definitions for the project view.

    """

    # A mapping from human-readable root names to globally unique Ids.
    aliases = {
        'NoSelectionMenu' : NO_SELECTION_MENU_ID,
        'ProjectMenu' : PROJECT_MENU_ID,
        }


#### EOF #####################################################################

