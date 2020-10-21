# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
Tests for ProjectPlugin
"""
import unittest

from envisage.ui.single_project.project_plugin import ProjectPlugin


class TestProjectPlugin(unittest.TestCase):

    def test_default_my_preferences_pages(self):
        plugin = ProjectPlugin()
        self.assertEqual(len(plugin.my_preferences_pages), 1)