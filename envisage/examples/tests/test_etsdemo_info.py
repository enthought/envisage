# (C) Copyright 2007-2025 Enthought, Inc., Austin, TX
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

from envisage.examples._etsdemo_info import info


class TestETSDemoInfo(unittest.TestCase):
    def test_info(self):
        # input to info is currently just a placeholder
        response = info({})
        self.assertTrue(os.path.exists(response["root"]))
