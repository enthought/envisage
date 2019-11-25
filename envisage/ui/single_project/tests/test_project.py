# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import unittest

from envisage.ui.single_project.api import Project

class MyProject(Project):
    pass

class TestProject(unittest.TestCase):

    def test_get_project_location(self):
        # Given
        prj = MyProject(application=None)

        # When
        loc = prj.get_default_project_location(prj.application)

        # Then
        self.assertIsNotNone(loc)
        self.assertIsInstance(loc, str)
