# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import unittest

from traits.api import HasTraits, Supports
from traits.interface_checker import check_implements
from traitsui.api import ITreeNode

from envisage.ui.single_project.api import Project
from envisage.ui.single_project.view.project_view import EmptyProject


class MyProject(Project):
    pass


class MyView(HasTraits):
    tree_node = Supports(ITreeNode)


class TestProjectView(unittest.TestCase):
    def test_empty_project_adapts_to_i_tree_node(self):
        empty_project = EmptyProject()

        view = MyView()
        view.tree_node = empty_project

        adapted = view.tree_node
        check_implements(type(adapted), ITreeNode)

    def test_project_adapts_to_i_tree_node(self):
        my_project = MyProject()

        view = MyView()
        view.tree_node = my_project

        adapted = view.tree_node
        check_implements(type(adapted), ITreeNode)
