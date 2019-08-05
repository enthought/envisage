# (C) Copyright 2019 Enthought, Inc., Austin, TX
# All rights reserved.

import os
import shutil
import tempfile
import unittest

from envisage._compat import pickle
from envisage.ui.tasks.api import TasksApplication

requires_gui = unittest.skipIf(
    os.environ["ETS_TOOLKIT"] == "null",
    "Test requires a non-null GUI backend",
)


@requires_gui
class TestTasksApplication(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir)

    def test_layout_save_uses_protocol_2(self):
        # We use pickle protocol 2 by default, to allow compatibility
        # across Python versions.
        state_location = self.tmpdir

        # Create application, and set it up to exit as soon as it's launched.
        app = TasksApplication(state_location=state_location)
        app.on_trait_change(app.exit, "application_initialized")

        memento_file = os.path.join(state_location, "application_memento")
        self.assertFalse(os.path.exists(memento_file))
        app.run()
        self.assertTrue(os.path.exists(memento_file))

        # Check that the generated file has protocol 2.
        with open(memento_file, "rb") as f:
            protocol_bytes = f.read(2)
        self.assertEqual(protocol_bytes, b"\x80\x02")

    @unittest.skipUnless(
        3 <= pickle.HIGHEST_PROTOCOL, "Test uses pickle protocol 3")
    def test_layout_save_with_protocol_3(self):
        # Test that the protocol can be overridden on a per-application basis.
        state_location = self.tmpdir

        # Create application, and set it up to exit as soon as it's launched.
        app = TasksApplication(
            state_location=state_location,
            layout_save_protocol=3,
        )
        app.on_trait_change(app.exit, "application_initialized")

        memento_file = os.path.join(state_location, "application_memento")
        self.assertFalse(os.path.exists(memento_file))
        app.run()
        self.assertTrue(os.path.exists(memento_file))

        # Check that the generated file uses protocol 3.
        with open(memento_file, "rb") as f:
            protocol_bytes = f.read(2)
        self.assertEqual(protocol_bytes, b"\x80\x03")
