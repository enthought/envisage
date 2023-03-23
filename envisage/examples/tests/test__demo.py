# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import os
import sys
import unittest

from envisage.examples._demo import demo_path


class TestDemoUtilities(unittest.TestCase):
    """Test utility functions in the _demo module."""

    def test_sys_path_inserted(self):
        path = os.path.join("dirname", "file.py")
        with demo_path(path):
            self.assertIn("dirname", sys.path)
        self.assertNotIn("dirname", sys.path)
