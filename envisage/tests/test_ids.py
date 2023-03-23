# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
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
            "PREFERENCES_CATEGORIES",
            "PREFERENCES_PANES",
            "TASKS",
            "TASK_EXTENSIONS",
        ]

        for extension_point_id in extension_point_ids:
            id_value = getattr(envisage.ids, extension_point_id)
            self.assertIsInstance(id_value, str)

    def test_id_strings_against_plugin_constants(self):
        # Check extension point IDs against ground truth on plugins
        self.check_id_against_plugin("PREFERENCES", CorePlugin)
        self.check_id_against_plugin("SERVICE_OFFERS", CorePlugin)
        self.check_id_against_plugin("BINDINGS", PythonShellPlugin)
        self.check_id_against_plugin("COMMANDS", PythonShellPlugin)
        self.check_id_against_plugin("PREFERENCES_CATEGORIES", TasksPlugin)
        self.check_id_against_plugin("PREFERENCES_PANES", TasksPlugin)
        self.check_id_against_plugin("TASKS", TasksPlugin)
        self.check_id_against_plugin("TASK_EXTENSIONS", TasksPlugin)

    def check_id_against_plugin(self, id_string, plugin_klass):
        """
        Check that the value of an id string matches that of a class variable.

        Parameters
        ----------
        id_string : str
            Identifier for the id.
        plugin_klass : type
            The Plugin subclass to check.
        """
        self.assertEqual(
            getattr(envisage.ids, id_string), getattr(plugin_klass, id_string)
        )
