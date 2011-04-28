#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
A Data resource type plugin.

"""

# Enthought library imports.
from envisage import PluginDefinition
from envisage.action.action_plugin_definition import \
    Group, Location, Menu
from envisage.action.default_action import DefaultAction
from envisage.core.core_plugin_definition import ApplicationObject
from envisage.resource.resource_plugin_definition \
    import ResourceType, ResourceManager
from envisage.plugins.python_shell.python_shell_plugin_definition import \
    Namespace

# Local imports.
from data.plugin.services import IDATA_MODEL, IDATA_UI
from data.plugin.data_action_set import DataActionSet


##############################################################################
# Constants
##############################################################################

# This plugin's globally unique identifier.  Our usage's assume this is the
# python path to the package containing the plugin definition module.
ID = 'data.plugin'


##############################################################################
# Extensions.
##############################################################################

#### Actions and ActionSets ##################################################


class RenameDataAction(DefaultAction):
    description = 'Rename this data.'
    name = '&Rename'

class EditDataAction(DefaultAction):
    description = 'Edit data properties.'
    name = '&Edit Data Properties'


data_action_set = DataActionSet(
    actions = [
#        # Data action group
#        DeleteDataAction(
#            locations = [
#                Location(
#                    after='RenameData',
#                    path='DataContextMenu/ActionGroup',
#                    ),
#                ],
#            ),
        RenameDataAction(
            locations = [
                Location(path='DataContextMenu/ActionGroup'),
                ],
            ),
        EditDataAction(
            locations = [
                Location(path='DataContextMenu/ActionGroup'),
                ],
            ),
        ],

    groups = [
        # Data groups
        Group(
            id = 'ActionGroup',
            location = Location(
                # after='PersistenceGroup',
                path='DataContextMenu',
                ),
            ),
        ],

    id = '%s.data_action_set.Default' % ID,
    name = 'DataPlugin',
    )


#### Application Objects #####################################################

model_service = ApplicationObject(
    class_name = '%s.model_service.ModelService' % ID,
    uol = 'service://' + IDATA_MODEL,
    )

ui_service = ApplicationObject(
    class_name = '%s.ui_service.UiService' % ID,
    kw = {'model_service' : model_service.uol},
    uol = 'service://' + IDATA_UI,
    )


#### Resource Types ##########################################################

# References to other plugin's resource types
FOLDER = 'envisage.resource.folder_resource_type.FolderResourceType'
INSTANCE = ('envisage.resource.instance_resource_type.'
    'InstanceResourceType')

# References to our resource types
DATA_TYPE = ID + '.resource_type.data_resource_type.DataResourceType'

resource_types = ResourceManager(
    resource_types = [
        ResourceType(
            class_name = DATA_TYPE,
            #precedes = [FOLDER, INSTANCE],
            ),
        ],
    )


#### Shell Namespace #########################################################

# Import template code into the shell for scripting.
#namespace = Namespace(
#    commands = [
#        'from cp.data.api import *',
#        ]
#    )


##############################################################################
# The plugin definition.
##############################################################################

class DataPlugin(PluginDefinition):
    # The plugin's globally unique identifier.
    id = ID

    # General information about the plugin.
    name = 'Data Plugin'
    version = '0.0.1'
    provider_name = 'Enthought Inc'
    provider_url = 'www.enthought.com'
    autostart = True

    # The Id's of the plugins that this plugin requires.
    requires = [
        ]

    # The extension points offered by this plugin.
    extension_points = [
        DataActionSet,
        ]

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [
        model_service,
        # namespace,
        resource_types,
        ui_service,
        data_action_set,
        ]


#### EOF #####################################################################

