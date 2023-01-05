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


class TestWorkbenchDefaultAction(unittest.TestCase):
    def test_workbench_default_action(self):
        import envisage.ui.workbench.default_action_set  # noqa: F401
