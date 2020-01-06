# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" This module redefines the Extension Point IDs and Service IDs defined by
Plugins provided by Envisage. Note that this module does not contain IDs
defined by all of the Plugins available in envisage.
The Plugins themselves remain the ground truth for the IDs. This module is
simply a convenient location from which the user can import the IDs.
"""

#### Extension Points #########################################################

# Extension Points defined by the CorePlugin.
PREFERENCES = 'envisage.preferences'
SERVICE_OFFERS = 'envisage.service_offers'

# Extension Points defined by the PythonShellPlugin.
# NOTE : The other PythonShellPlugin defines extension points with the same ID.
BINDINGS = 'envisage.plugins.python_shell.bindings'
COMMANDS = 'envisage.plugins.python_shell.commands'

# Extension Points defined by the IPythonKernelPlugin.
IPYTHON_NAMESPACE = 'ipython_plugin.namespace'

# Extension Points defined by the TasksPlugin.
PREFERENCES_CATEGORIES = 'envisage.ui.tasks.preferences_categories'
PREFERENCES_PANES = 'envisage.ui.tasks.preferences_panes'
TASKS = 'envisage.ui.tasks.tasks'
TASK_EXTENSIONS = 'envisage.ui.tasks.task_extensions'

#### Services ################################################################

# Services offered by the IPythonKernelPlugin
IPYTHON_KERNEL_PROTOCOL = 'envisage.plugins.ipython_kernel.internal_ipkernel.InternalIPKernel'  # noqa: E501
