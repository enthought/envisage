# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest

import envisage.ids
from envisage.api import CorePlugin
from envisage.plugins.ipython_kernel.api import IPythonKernelPlugin
from envisage.plugins.python_shell.python_shell_plugin import PythonShellPlugin
from envisage.ui.tasks.api import TasksPlugin


class TestIds(unittest.TestCase):
    def test_id_strings(self):
        extension_point_ids = [
            # Extension point IDs
            "PREFERENCES",
            "SERVICE_OFFERS",
            "BINDINGS",
            "COMMANDS",
            "IPYTHON_NAMESPACE",
            "PREFERENCES_CATEGORIES",
            "PREFERENCES_PANES",
            "TASKS",
            "TASK_EXTENSIONS",
            # Service IDs
            "IPYTHON_KERNEL_PROTOCOL",
        ]

        for extension_point_id in extension_point_ids:
            id_value = getattr(envisage.ids, extension_point_id)
            self.assertIsInstance(id_value, str)

    def test_id_strings_against_plugin_constants(self):
        def check_id_against_plugin(id_string, plugin_klass):
            self.assertEqual(
                getattr(envisage.ids, id_string),
                getattr(plugin_klass, id_string)
            )

        # Check extension point IDs against ground truth on plugins
        check_id_against_plugin("PREFERENCES", CorePlugin)
        check_id_against_plugin("SERVICE_OFFERS", CorePlugin)
        check_id_against_plugin("BINDINGS", PythonShellPlugin)
        check_id_against_plugin("COMMANDS", PythonShellPlugin)
        check_id_against_plugin("IPYTHON_NAMESPACE", IPythonKernelPlugin)
        check_id_against_plugin("PREFERENCES_CATEGORIES", TasksPlugin)
        check_id_against_plugin("PREFERENCES_PANES", TasksPlugin)
        check_id_against_plugin("TASKS", TasksPlugin)
        check_id_against_plugin("TASK_EXTENSIONS", TasksPlugin)

        # Check service IDs against ground truth on plugins
        check_id_against_plugin("IPYTHON_KERNEL_PROTOCOL", IPythonKernelPlugin)
