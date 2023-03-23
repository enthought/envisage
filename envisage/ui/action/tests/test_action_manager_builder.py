# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the action manager builder. """

# Standard library imports.
import unittest

# Enthought library imports.
from envisage.ui.action.api import Action, ActionSet, Group, Menu

# Local imports.
from .dummy_action_manager_builder import DummyActionManagerBuilder


class ActionManagerBuilderTestCase(unittest.TestCase):
    """Tests for the action manager builder."""

    def test_action_with_nonexistent_group(self):
        """action with non-existent group"""

        action_sets = [
            ActionSet(
                actions=[
                    Action(
                        class_name="Exit", path="MenuBar/File", group="Bogus"
                    ),
                ]
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        with self.assertRaises(ValueError):
            builder.create_menu_bar_manager("MenuBar")

    def test_action_with_nonexistent_sibling(self):
        """action with non-existent sibling"""

        action_sets = [
            ActionSet(
                actions=[
                    Action(
                        class_name="Exit",
                        path="MenuBar/File",
                        before="NonExistentAction",
                    ),
                ]
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        with self.assertRaises(ValueError):
            builder.create_menu_bar_manager("MenuBar")

    def test_group_with_nonexistent_sibling(self):
        """group with non-existent sibling"""

        action_sets = [
            ActionSet(
                groups=[
                    Group(id="FileMenuGroup", path="MenuBar", before="Bogus")
                ]
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        with self.assertRaises(ValueError):
            builder.create_menu_bar_manager("MenuBar")

    def test_menu_with_nonexistent_sibling(self):
        """menu with non-existent sibling"""

        action_sets = [
            ActionSet(
                menus=[Menu(name="&File", path="MenuBar", before="Bogus")]
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        with self.assertRaises(ValueError):
            builder.create_menu_bar_manager("MenuBar")

    def test_action_with_path_component_that_is_not_a_menu(self):
        """action with path component that is not a menu"""

        action_sets = [
            ActionSet(
                actions=[
                    Action(class_name="Exit", path="MenuBar/File"),
                    Action(class_name="Broken", path="MenuBar/File/Exit"),
                ]
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        with self.assertRaises(ValueError):
            builder.create_menu_bar_manager("MenuBar")

    def test_single_top_level_menu_with_no_group(self):
        """single top level menu with no group"""

        action_sets = [ActionSet(menus=[Menu(name="&File", path="MenuBar")])]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_bar_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that the 'File' menu was added to the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_bar_manager.groups))

        group = menu_bar_manager.find_group("additions")
        ids = [item.id for item in group.items]
        self.assertEqual(["File"], ids)

    def test_single_top_level_group(self):
        """single top level group"""

        action_sets = [
            ActionSet(groups=[Group(id="FileMenuGroup", path="MenuBar")])
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_bar_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that the group was added before the 'additions' group.
        self.assertEqual(2, len(menu_bar_manager.groups))

        ids = [group.id for group in menu_bar_manager.groups]
        self.assertEqual(["FileMenuGroup", "additions"], ids)

    def test_top_level_menus_with_no_groups(self):
        """top level menus with_no groups"""

        action_sets = [
            ActionSet(
                menus=[
                    Menu(name="&File", path="MenuBar"),
                    Menu(name="&Edit", path="MenuBar"),
                    Menu(name="&Tools", path="MenuBar"),
                    Menu(name="&Help", path="MenuBar"),
                ],
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_bar_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar (and in the right order!).
        self.assertEqual(1, len(menu_bar_manager.groups))

        group = menu_bar_manager.find_group("additions")
        ids = [item.id for item in group.items]
        self.assertEqual(["File", "Edit", "Tools", "Help"], ids)

    def test_top_level_menus_no_groups_before_and_after(self):
        """top level menus no groups, before and after"""

        action_sets = [
            ActionSet(
                menus=[Menu(name="&Edit", path="MenuBar", after="File")],
            ),
            ActionSet(menus=[Menu(name="&File", path="MenuBar")]),
            ActionSet(menus=[Menu(name="&Help", path="MenuBar")]),
            ActionSet(
                menus=[Menu(name="&Tools", path="MenuBar", before="Help")],
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group("additions")
        ids = [item.id for item in additions.items]
        self.assertEqual(["File", "Edit", "Tools", "Help"], ids)

    def test_top_level_menu_non_existent_group(self):
        """top level menu non-existent group"""

        action_sets = [
            ActionSet(
                menus=[
                    Menu(name="&File", path="MenuBar", group="FileMenuGroup"),
                ],
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        with self.assertRaises(ValueError):
            builder.create_menu_bar_manager("MenuBar")

    def test_top_level_menu_group(self):
        """top level menu group"""

        action_sets = [
            ActionSet(
                groups=[Group(id="FileMenuGroup", path="MenuBar")],
                menus=[
                    Menu(name="&File", path="MenuBar", group="FileMenuGroup"),
                ],
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that the 'File' menu was added to the 'FileMenuGroup'
        # group of the menubar.
        self.assertEqual(2, len(menu_manager.groups))

        ids = [group.id for group in menu_manager.groups]
        self.assertEqual(["FileMenuGroup", "additions"], ids)

        group = menu_manager.find_group("FileMenuGroup")
        self.assertEqual("File", group.items[0].id)

    def test_sub_menus_no_groups(self):
        """sub-menus no groups"""

        # We split the contributions into different action sets just because
        # that is how it might end up in an actual application... not because
        # you *have* to split them up this way!
        action_sets = [
            ActionSet(
                menus=[
                    Menu(name="&File", path="MenuBar"),
                    Menu(name="&Edit", path="MenuBar"),
                    Menu(name="&Tools", path="MenuBar"),
                    Menu(name="&Help", path="MenuBar"),
                ],
            ),
            ActionSet(menus=[Menu(name="&New", path="MenuBar/File")]),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        additions = menu.find_group("additions")

        self.assertEqual("New", additions.items[0].id)

    def test_actions_no_groups(self):
        """actions no groups"""

        # We split the contributions into different action sets just because
        # that is how it might end up in an actual application... not because
        # you *have* to split them up this way!
        action_sets = [
            ActionSet(
                menus=[
                    Menu(name="&File", path="MenuBar"),
                    Menu(name="&Edit", path="MenuBar"),
                    Menu(name="&Tools", path="MenuBar"),
                    Menu(name="&Help", path="MenuBar"),
                ]
            ),
            ActionSet(
                actions=[
                    Action(class_name="Exit", path="MenuBar/File"),
                    Action(class_name="About", path="MenuBar/Help"),
                ]
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure the 'ExitAction' action got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        additions = menu.find_group("additions")

        self.assertEqual("Exit", additions.items[0].id)

        # Make sure the 'AboutAction' action got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item("Help")
        additions = menu.find_group("additions")

        self.assertEqual("About", additions.items[0].id)

    def test_actions_make_submenus(self):
        """actions make submenus"""

        action_sets = [
            ActionSet(
                actions=[
                    Action(class_name="Folder", path="MenuBar/File/New"),
                    Action(class_name="File", path="MenuBar/File/New"),
                ]
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure the 'File' menu got added to the 'additions' group of the
        # menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group("additions")
        self.assertEqual("File", additions.items[0].id)

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        additions = menu.find_group("additions")

        self.assertEqual("New", additions.items[0].id)

        # Make sure the new 'Folder' and 'File' actions got added to the
        # 'additions' group of the 'New' menu.
        menu = menu_manager.find_item("File/New")
        additions = menu.find_group("additions")

        self.assertEqual("Folder", additions.items[0].id)
        self.assertEqual("File", additions.items[1].id)

    def test_actions_make_submenus_before_and_after(self):
        """actions make submenus before and after"""

        action_sets = [
            ActionSet(
                actions=[
                    Action(
                        class_name="File",
                        path="MenuBar/File/New",
                        after="Folder",
                    ),
                    Action(
                        class_name="Project",
                        path="MenuBar/File/New",
                        before="Folder",
                    ),
                    Action(class_name="Folder", path="MenuBar/File/New"),
                ]
            )
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure the 'File' menu got added to the 'additions' group of the
        # menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group("additions")
        self.assertEqual("File", additions.items[0].id)

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        additions = menu.find_group("additions")

        self.assertEqual("New", additions.items[0].id)

        # Make sure the new 'Folder' and 'File' actions got added to the
        # 'additions' group of the 'New' menu.
        menu = menu_manager.find_item("File/New")
        additions = menu.find_group("additions")

        ids = [item.id for item in additions.items]
        self.assertEqual(["Project", "Folder", "File"], ids)

    def test_explicit_groups(self):
        """explicit groups"""

        action_sets = [
            ActionSet(
                menus=[
                    Menu(name="&File", path="MenuBar"),
                    Menu(name="&Edit", path="MenuBar"),
                    Menu(name="&Tools", path="MenuBar"),
                    Menu(name="&Help", path="MenuBar"),
                ],
            ),
            ActionSet(
                menus=[
                    Menu(name="&New", path="MenuBar/File", group="NewGroup"),
                ],
            ),
            ActionSet(
                actions=[
                    Action(
                        class_name="Exit",
                        path="MenuBar/File",
                        group="ExitGroup",
                    ),
                ]
            ),
            ActionSet(
                groups=[
                    Group(id="ExitGroup", path="MenuBar/File"),
                    Group(
                        id="SaveGroup", path="MenuBar/File", after="NewGroup"
                    ),
                    Group(
                        id="NewGroup", path="MenuBar/File", before="ExitGroup"
                    ),
                ]
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group("additions")
        ids = [item.id for item in additions.items]
        self.assertEqual(["File", "Edit", "Tools", "Help"], ids)

        # Make sure the 'File' menu has got 3 groups, 'NewGroup', 'ExitGroup'
        # and 'additions' (and in that order!).
        menu = menu_manager.find_item("File")
        self.assertEqual(4, len(menu.groups))

        ids = [group.id for group in menu.groups]
        self.assertEqual(
            ["NewGroup", "SaveGroup", "ExitGroup", "additions"], ids
        )

        # Make sure the 'New' sub-menu got added to the 'NewGroup' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        group = menu.find_group("NewGroup")

        self.assertEqual("New", group.items[0].id)

        # Make sure the 'Exit' action got added to the 'ExitGroup' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        group = menu.find_group("ExitGroup")

        self.assertEqual("Exit", group.items[0].id)

    def test_actions_and_menus_in_groups(self):
        """actions and menus in groups"""

        action_sets = [
            ActionSet(
                menus=[
                    Menu(
                        name="&File",
                        path="MenuBar",
                        groups=[
                            Group(
                                id="NewGroup",
                                path="MenuBar/File",
                                before="ExitGroup",
                            ),
                            Group(id="ExitGroup", path="MenuBar/File"),
                        ],
                    ),
                    Menu(name="&Edit", path="MenuBar"),
                    Menu(name="&Tools", path="MenuBar"),
                    Menu(name="&Help", path="MenuBar"),
                ],
            ),
            ActionSet(
                menus=[
                    Menu(name="&New", path="MenuBar/File", group="NewGroup"),
                ],
            ),
            ActionSet(
                actions=[
                    Action(
                        class_name="Exit",
                        path="MenuBar/File",
                        group="ExitGroup",
                    ),
                ]
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group("additions")
        ids = [item.id for item in additions.items]
        self.assertEqual(["File", "Edit", "Tools", "Help"], ids)

        # Make sure the 'File' menu has got 3 groups, 'NewGroup', 'ExitGroup'
        # and 'additions' (and in that order!).
        menu = menu_manager.find_item("File")
        self.assertEqual(3, len(menu.groups))

        ids = [group.id for group in menu.groups]
        self.assertEqual(["NewGroup", "ExitGroup", "additions"], ids)

        # Make sure the 'New' sub-menu got added to the 'NewGroup' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        group = menu.find_group("NewGroup")

        self.assertEqual("New", group.items[0].id)

        # Make sure the 'Exit' action got added to the 'ExitGroup' group
        # of the 'File' menu.
        menu = menu_manager.find_item("File")
        group = menu.find_group("ExitGroup")

        self.assertEqual("Exit", group.items[0].id)

    def test_duplicate_menu(self):
        """duplicate menu"""

        action_sets = [
            ActionSet(
                menus=[
                    Menu(
                        name="&File",
                        path="MenuBar",
                        groups=[
                            Group(id="NewGroup", path="MenuBar/File"),
                            Group(id="ExitGroup", path="MenuBar/File"),
                        ],
                    ),
                ],
            ),
            ActionSet(
                menus=[
                    Menu(
                        name="&File",
                        path="MenuBar",
                        groups=[
                            Group(id="ExtraGroup", path="MenuBar/File"),
                        ],
                    ),
                ],
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        # Make sure we only get *one* 'File' menu.
        additions = menu_manager.find_group("additions")
        ids = [item.id for item in additions.items]
        self.assertEqual(["File"], ids)

        # Make sure the 'File' menu has got 4 groups, 'NewGroup', 'ExitGroup',
        # 'ExtraGroup' and 'additions' (and in that order!).
        menu = menu_manager.find_item("File")
        self.assertEqual(4, len(menu.groups))

        ids = [group.id for group in menu.groups]
        self.assertEqual(
            ["NewGroup", "ExitGroup", "ExtraGroup", "additions"], ids
        )

    def test_duplicate_group(self):
        """duplicate group"""

        action_sets = [
            ActionSet(
                menus=[
                    Menu(
                        name="&File",
                        path="MenuBar",
                        groups=[
                            Group(id="NewGroup", path="MenuBar/File"),
                            Group(id="ExitGroup", path="MenuBar/File"),
                        ],
                    ),
                ],
            ),
            ActionSet(
                menus=[
                    Menu(
                        name="&File",
                        path="MenuBar",
                        groups=[
                            Group(id="NewGroup", path="MenuBar/File"),
                        ],
                    ),
                ],
            ),
        ]

        # Create a builder containing the action set.
        builder = DummyActionManagerBuilder(action_sets=action_sets)

        # Create a menu bar manager for the 'MenuBar'.
        menu_manager = builder.create_menu_bar_manager("MenuBar")

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        # Make sure we only get *one* 'File' menu.
        additions = menu_manager.find_group("additions")
        ids = [item.id for item in additions.items]
        self.assertEqual(["File"], ids)

        # Make sure the 'File' menu has got 3 groups, 'NewGroup', 'ExitGroup'
        # and 'additions' (and in that order!).
        menu = menu_manager.find_item("File")
        self.assertEqual(3, len(menu.groups))

        ids = [group.id for group in menu.groups]
        self.assertEqual(["NewGroup", "ExitGroup", "additions"], ids)
