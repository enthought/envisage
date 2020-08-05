# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" This module redefines the Extension Point IDs and Service IDs defined on
Plugins provided by Envisage. Note that this module does not contain IDs
defined by all of the Plugins available in Envisage.

The Plugins themselves remain the ground truth for the IDs. This module is
simply a convenient location from which the user can import the IDs.
"""

#### Extension Points #########################################################

#: Ext. Pt. to contribute preference files, defined on the ``CorePlugin``.
PREFERENCES = 'envisage.preferences'

#: Ext. Pt. to contribute ``ServiceOffer`` s, defined on the ``CorePlugin``.
SERVICE_OFFERS = 'envisage.service_offers'

# NOTE : The other PythonShellPlugin defines extension points with the same ID.
#: Ext. Pt. to contribute name/value pairs that will be bound to the
#: ``PythonShell``, defined on the ``PythonShellPlugin``.
BINDINGS = 'envisage.plugins.python_shell.bindings'

#: Ext. Pt. to contribute commands that will be executed in the
#: ``PythonShell``, defined on the ``PythonShellPlugin``.
COMMANDS = 'envisage.plugins.python_shell.commands'

#: Ext. Pt. to contribute name/value pairs that will be bound to the
#: ``IPythonShell``, defined on the ``IPythonKernelPlugin``.
IPYTHON_NAMESPACE = 'ipython_plugin.namespace'

#: Ext. Pt. to contribute preferences categories, defined on the
#: ``TasksPlugin``.
PREFERENCES_CATEGORIES = 'envisage.ui.tasks.preferences_categories'

#: Ext. Pt. to contribute preference panes, defined on the ``TasksPlugin``.
PREFERENCES_PANES = 'envisage.ui.tasks.preferences_panes'

#: Ext. Pt. to contribute task factories, defined on the ``TasksPlugin``.
TASKS = 'envisage.ui.tasks.tasks'

#: Ext. Pt. to contribute task extensions, defined on the ``TasksPlugin``.
TASK_EXTENSIONS = 'envisage.ui.tasks.task_extensions'

#### Services ################################################################

#: Service to access the active ``InternalIPKernel`` instance in the
#: application, defined on the ``IPythonKernelPlugin``.
IPYTHON_KERNEL_PROTOCOL = 'envisage.plugins.ipython_kernel.internal_ipkernel.InternalIPKernel'  # noqa: E501
