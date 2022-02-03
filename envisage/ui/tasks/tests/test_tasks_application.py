# (C) Copyright 2007-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os
import unittest

import pkg_resources

from envisage.ui.tasks.api import TasksApplication
from pyface.i_gui import IGUI
from traits.api import HasTraits, provides

requires_gui = unittest.skipIf(
    os.environ.get("ETS_TOOLKIT", "none") in {"null", "none"},
    "Test requires a non-null GUI backend",
)


@provides(IGUI)
class DummyGUI(HasTraits):
    pass


@requires_gui
class TestTasksApplication(unittest.TestCase):
    def test_layout_load(self):
        # Check we can load a previously-created state. That previous state
        # has an main window size of (492, 743) (to allow us to check that
        # we're actually using the file).
        stored_state_location = pkg_resources.resource_filename(
            "envisage.ui.tasks.tests", "data"
        )
        app = TasksApplication(state_location=stored_state_location)
        app.on_trait_change(app.exit, "application_initialized")
        app.run()
