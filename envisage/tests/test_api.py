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

import envisage.api as api
import envisage.ids as ids


class TestApi(unittest.TestCase):
    """Test for API"""

    def test_import(self):
        self.assertEqual(api.BINDINGS, ids.BINDINGS)
        self.assertEqual(api.COMMANDS, ids.COMMANDS)
        self.assertEqual(api.PREFERENCES, ids.PREFERENCES)
        self.assertEqual(
            api.PREFERENCES_CATEGORIES, ids.PREFERENCES_CATEGORIES
        )
        self.assertEqual(api.PREFERENCES_PANES, ids.PREFERENCES_PANES)
        self.assertEqual(api.SERVICE_OFFERS, ids.SERVICE_OFFERS)
        self.assertEqual(api.TASKS, ids.TASKS)
        self.assertEqual(api.TASK_EXTENSIONS, ids.TASK_EXTENSIONS)
