# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Standard library imports.
import os.path

from traits.api import List

# Enthought library imports.
from envisage.api import Plugin
from envisage.ui.tasks.api import TaskFactory


class AttractorsPlugin(Plugin):
    """The chaotic attractors plugin."""

    # Extension point IDs.
    PREFERENCES = "envisage.preferences"
    PREFERENCES_PANES = "envisage.ui.tasks.preferences_panes"
    TASKS = "envisage.ui.tasks.tasks"

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = "example.attractors"

    # The plugin's name (suitable for displaying to the user).
    name = "Attractors"

    #### Contributions to extension points made by this plugin ################

    preferences = List(contributes_to=PREFERENCES)
    preferences_panes = List(contributes_to=PREFERENCES_PANES)
    tasks = List(contributes_to=TASKS)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _preferences_default(self):
        filename = os.path.join(os.path.dirname(__file__), "preferences.ini")
        return ["file://" + filename]

    def _preferences_panes_default(self):
        from attractors.attractors_preferences import AttractorsPreferencesPane

        return [AttractorsPreferencesPane]

    def _tasks_default(self):
        from attractors.visualize_2d_task import Visualize2dTask
        from attractors.visualize_3d_task import Visualize3dTask

        return [
            TaskFactory(
                id="example.attractors.task_2d",
                name="2D Visualization",
                factory=Visualize2dTask,
            ),
            TaskFactory(
                id="example.attractors.task_3d",
                name="3D Visualization",
                factory=Visualize3dTask,
            ),
        ]
