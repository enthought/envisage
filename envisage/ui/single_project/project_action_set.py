# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Single project action set. """
# Enthought library imports.
from envisage.ui.action.api import Action, Group, Menu, ToolBar
from envisage.ui.workbench.api import WorkbenchActionSet

# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])

class ProjectActionSet(WorkbenchActionSet):
    """ Action set of a default Project. """

    # The action set's globally unique identifier.
    id = 'envisage.ui.single_project.action_set'

    # List of menus we provide.
    menus = [
        Menu(
            id='ProjectMenu',
            name='&Project',
            path='MenuBar/File',
            group='ProjectGroup',
        ),
    ]

    # List of groups we provide.
    groups = [
        Group(
            id='OpenGroup',
            path='MenuBar/File/ProjectMenu'
        ),
        Group(
            id='SaveGroup',
            path='MenuBar/File/ProjectMenu'
        ),
        Group(
            id='CloseGroup',
            path='MenuBar/File/ProjectMenu'
        ),
        Group(
            id='ProjectGroup',
            path='MenuBar/File',
            before='ExitGroup'
        ),
    ]

    # List of toolbars we provide.
    tool_bars = [
        ToolBar(
            name='Project',
            groups=['PerspectiveGroup', 'ProjectGroup']
        ),
    ]

    # List of actions we provide.
    actions = [
        # File menu actions.
        Action(
            class_name=PKG + '.action.api:NewProjectAction',
            group='OpenGroup',
            path='MenuBar/File/ProjectMenu',
        ),
        Action(
            class_name=PKG + '.action.api:OpenProjectAction',
            group='OpenGroup',
            path='MenuBar/File/ProjectMenu',
        ),
        Action(
            class_name=PKG + '.action.api:SaveProjectAction',
            group='SaveGroup',
            path='MenuBar/File/ProjectMenu',
        ),
        Action(
            class_name=PKG + '.action.api:SaveAsProjectAction',
            group='SaveGroup',
            path='MenuBar/File/ProjectMenu',
        ),
        Action(
            class_name=PKG + '.action.api:CloseProjectAction',
            group='CloseGroup',
            path='MenuBar/File/ProjectMenu',
        ),

        # Toolbar actions.
        Action(
            class_name=PKG + '.action.api:SwitchToAction',
            group='PerspectiveGroup',
            path='ToolBar/Project',
        ),
        Action(
            class_name=PKG + '.action.api:NewProjectAction',
            group='ProjectGroup',
            path='ToolBar/Project',
        ),
        Action(
            class_name=PKG + '.action.api:OpenProjectAction',
            group='ProjectGroup',
            path='ToolBar/Project',
        ),
        Action(
            class_name=PKG + '.action.api:SaveProjectAction',
            group='ProjectGroup',
            path='ToolBar/Project',
        ),
        Action(
            class_name=PKG + '.action.api:SaveAsProjectAction',
            group='ProjectGroup',
            path='ToolBar/Project',
        ),
        Action(
            class_name=PKG + '.action.api:CloseProjectAction',
            group='ProjectGroup',
            path='ToolBar/Project',
        ),
    ]

    #### 'WorkbenchActionSet' interface #######################################

    # The Ids of the perspectives that the action set is enabled in.
    enabled_for_perspectives = ['Project']

    # The Ids of the perspectives that the action set is visible in.
    visible_for_perspectives = ['Project']
