# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""Tests for action sets."""

import unittest

from envisage.ui.action.api import ActionSet

LOGGER_NAME = "envisage.ui.action.action_set"


class ActionSetTestCase(unittest.TestCase):
    """Tests for action sets."""

    def test_default_id_is_not_reported_as_a_warning(self):
        """default id is logged below warning level"""

        # Defaulting the id is normal, supported behaviour, so there's no
        # action for the user to take. See enthought/envisage#574.
        with self.assertLogs(LOGGER_NAME, level="INFO") as watcher:
            self.assertEqual(
                "envisage.ui.action.action_set.ActionSet", ActionSet().id
            )

        self.assertEqual(
            ["INFO"], [record.levelname for record in watcher.records]
        )

    def test_default_name_is_not_reported_as_a_warning(self):
        """default name is logged below warning level"""

        with self.assertLogs(LOGGER_NAME, level="INFO") as watcher:
            self.assertEqual("Action Set", ActionSet().name)

        self.assertEqual(
            ["INFO"], [record.levelname for record in watcher.records]
        )
