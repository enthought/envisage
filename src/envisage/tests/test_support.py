# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""Tests for the test support utilities themselves."""

import os
import unittest

from envisage.tests.support import (
    gui_available,
    gui_skip_reason,
    pyside6_available,
)


class GuiAvailableTestCase(unittest.TestCase):
    def test_gui_available_when_a_toolkit_is_installed(self):
        # Pyface falls back to its null toolkit when Qt can't be imported,
        # which makes every GUI test skip without anything failing. That's
        # usually a missing system library rather than a deliberate choice,
        # so treat it as an error instead of letting the skips pass unnoticed.
        if not pyside6_available:
            self.skipTest("PySide6 is not installed")
        if os.environ.get("ETS_TOOLKIT") == "null":
            self.skipTest("The null toolkit was requested explicitly")

        self.assertTrue(
            gui_available,
            "PySide6 is installed, but Pyface fell back to the null toolkit "
            "({}). A system library needed to import Qt is probably "
            "missing.".format(gui_skip_reason),
        )
