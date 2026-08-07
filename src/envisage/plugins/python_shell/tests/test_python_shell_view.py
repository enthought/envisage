# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the Python shell view. """

# Standard library imports.
import sys
import unittest

# Enthought library imports.
from envisage.api import Application
from envisage.plugins.python_shell.api import IPythonShell
from envisage.plugins.python_shell.view.api import PythonShellView
from envisage.tests.support import requires_gui
from envisage.ui.workbench.api import Workbench, WorkbenchWindow


def create_window():
    """A workbench window with an application behind it.

    'WorkbenchWindow.application' delegates to the workbench, so it is the
    workbench that has to carry it.
    """
    return WorkbenchWindow(
        workbench=Workbench(application=Application(id="test"))
    )


@requires_gui
class PythonShellViewTestCase(unittest.TestCase):
    def test_create_control(self):
        """The view builds its shell and registers itself as a service."""
        window = create_window()
        view = PythonShellView(window=window)
        stdout = sys.stdout

        control = view.create_control(None)
        try:
            self.assertIsNotNone(control)
            self.assertIsNotNone(
                view.window.application.get_service(IPythonShell)
            )
            # reaches the interpreter behind the 'namespace' property
            view.bind("answer", 42)
            self.assertEqual(view.namespace["answer"], 42)
        finally:
            view.destroy_control()

        self.assertIs(sys.stdout, stdout)
        self.assertIsNone(window.application.get_service(IPythonShell))

    def test_destroy_control_without_create_control(self):
        """Tearing down a view whose 'create_control' never ran is quiet.

        Pyface's 'WorkbenchWindowLayout.add_view' does exactly this when
        'create_control' raises, so anything raised here replaces the error
        that explains the failure.
        """
        PythonShellView(window=create_window()).destroy_control()

    def test_destroy_control_is_repeatable(self):
        """A second 'destroy_control' has nothing left to undo."""
        view = PythonShellView(window=create_window())
        view.create_control(None)
        view.destroy_control()
        stdout = sys.stdout

        view.destroy_control()

        self.assertIs(sys.stdout, stdout)
