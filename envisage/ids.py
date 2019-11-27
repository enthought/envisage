# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from envisage.core_plugin import CorePlugin
from envisage.plugins.ipython_kernel.ipython_kernel_plugin import IPythonKernelPlugin
from envisage.plugins.python_shell.python_shell_plugin import PythonShellPlugin
from envisage.ui.single_project.project_plugin import ProjectPlugin
from envisage.ui.tasks.tasks_plugin import TasksPlugin
from envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

#### Extension Points #########################################################

# Extension Points defined by the CorePlugin.
CLASS_LOAD_HOOKS = CorePlugin.CLASS_LOAD_HOOKS
PREFERENCES = CorePlugin.PREFERENCES
SERVICE_OFFERS = CorePlugin.SERVICE_OFFERS

# Extension Points defined by the PythonShellPlugin.
# NOTE : The other PythonShellPlugin defines extension points with the same ID.
BINDINGS = PythonShellPlugin.BINDINGS
COMMANDS = PythonShellPlugin.COMMANDS

# Extension Points defined by the IPythonKernelPlugin.
IPYTHON_NAMESPACE = IPythonKernelPlugin.IPYTHON_NAMESPACE

# Extension Points defined by the ProjectPlugin.
FACTORY_DEFINITIONS = ProjectPlugin.FACTORY_DEFINITIONS
UI_SERVICE_FACTORY = ProjectPlugin.UI_SERVICE_FACTORY

# Extension Points defined by the TasksPlugin.
PREFERENCES_CATEGORIES = TasksPlugin.PREFERENCES_CATEGORIES
PREFERENCES_PANES = TasksPlugin.PREFERENCES_PANES
TASKS = TasksPlugin.TASKS
TASK_EXTENSIONS = TasksPlugin.TASK_EXTENSIONS

# Extension Points defined by the WorkbenchPlugin.
ACTION_SETS = WorkbenchPlugin.ACTION_SETS
PERSPECTIVES = WorkbenchPlugin.PERSPECTIVES
PREFERENCES_PAGES = WorkbenchPlugin.PREFERENCES_PAGES
WORKBENCH_SERVICE_OFFERS = WorkbenchPlugin.WORKBENCH_SERVICE_OFFERS
VIEWS = WorkbenchPlugin.VIEWS

# Ensure that a `from envisage.ids import *` import only brings in ids.
del CorePlugin
del IPythonKernelPlugin
del PythonShellPlugin
del ProjectPlugin
del TasksPlugin
del WorkbenchPlugin
