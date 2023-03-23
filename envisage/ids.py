# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" This module redefines the Extension Point IDs and Service IDs defined on
Plugins provided by Envisage. Note that this module does not contain IDs
defined by all of the Plugins available in Envisage.

The Plugins themselves remain the ground truth for the IDs. This module is
simply a convenient location from which the user can import the IDs.
"""

#### Extension Points #########################################################

#: Extension Point to contribute preference files, defined on the
#: ``CorePlugin``.
PREFERENCES = "envisage.preferences"

#: Extension Point to contribute ``ServiceOffer`` s, defined on the
#: ``CorePlugin``.
SERVICE_OFFERS = "envisage.service_offers"

# NOTE : The other PythonShellPlugin defines extension points with the same ID.
#: Extension Point to contribute name/value pairs that will be bound to the
#: ``PythonShell``, defined on the ``PythonShellPlugin``.
BINDINGS = "envisage.plugins.python_shell.bindings"

#: Extension Point to contribute commands that will be executed in the
#: ``PythonShell``, defined on the ``PythonShellPlugin``.
COMMANDS = "envisage.plugins.python_shell.commands"

#: Extension Point to contribute preferences categories, defined on the
#: ``TasksPlugin``.
PREFERENCES_CATEGORIES = "envisage.ui.tasks.preferences_categories"

#: Extension Point to contribute preference panes, defined on the
#: ``TasksPlugin``.
PREFERENCES_PANES = "envisage.ui.tasks.preferences_panes"

#: Extension Point to contribute task factories, defined on the
#: ``TasksPlugin``.
TASKS = "envisage.ui.tasks.tasks"

#: Extension Point to contribute task extensions, defined on the
#: ``TasksPlugin``.
TASK_EXTENSIONS = "envisage.ui.tasks.task_extensions"
