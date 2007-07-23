""" Tests for the menu builder. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.ui.action.api import Action, ActionSet, Group, Location
from enthought.envisage.ui.action.api import Menu, MenuBuilder


class TestMenuBuilder(MenuBuilder):
    """ A test menu builder that doesn't build real actions! """

    ###########################################################################
    # Protected 'MenuBuilder' interface.
    ###########################################################################

    def _create_action(self, action_definition):
        """ Creates an action implementation from an action definitions. """

        from enthought.pyface.action.api import Action
        return Action(name=action_definition.class_name)

    def _create_group(self, group_definition):
        """ Creates a group implementation from a group definitions. """

        from enthought.pyface.action.api import Group
        return Group(id=group_definition.id)

    def _create_menu_manager(self, menu_definition):
        """ Creates a menu manager implementation from a menu extension. """

        from enthought.pyface.action.api import Group, MenuManager
        menu_manager = MenuManager(id=menu_definition.id)
        for group_definition in menu_definition.groups:
            menu_manager.insert(-1, Group(id=group_definition.id))

        return menu_manager

    
class MenuBuilderTestCase(unittest.TestCase):
    """ Tests for the menu builder. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_top_level_menus_no_groups(self):
        """ top level menus no groups """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', path='MenuBar'),
                    Menu(name='&Edit', path='MenuBar'),
                    Menu(name='&Tools', path='MenuBar'),
                    Menu(name='&Help', path='MenuBar')
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group('additions')
        ids = [item.id for item in additions.items]
        self.assertEqual(['File', 'Edit', 'Tools', 'Help'], ids)

        return

    def test_top_level_menus_no_groups_before_and_after(self):
        """ top level menus no groups, before and after """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&Edit', path='MenuBar', after='File'),
                ],
            ),

            ActionSet(
                menus = [
                    Menu(name='&File', path='MenuBar'),
                ],
            ),

            ActionSet(
                menus = [
                    Menu(name='&Help', path='MenuBar')
                ],
            ),

            ActionSet(
                menus = [
                    Menu(name='&Tools', path='MenuBar', before='Help'),
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group('additions')
        ids = [item.id for item in additions.items]
        self.assertEqual(['File', 'Edit', 'Tools', 'Help'], ids)

        return

    def test_top_level_menu_non_existent_group(self):
        """ top level menu non-existent group """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', path='MenuBar', group='FileMenuGroup'),
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        self.failUnlessRaises(
            ValueError, menu_builder.create_menu_bar_manager, 'MenuBar'
        )

        return

    def test_top_level_menu_group(self):
        """ top level menu group """

        action_sets = [
            ActionSet(
                groups = [
                    Group(id='FileMenuGroup', path='MenuBar')
                ],
                
                menus = [
                    Menu(name='&File', path='MenuBar', group='FileMenuGroup'),
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure that the 'File' menu was added to the 'FileMenuGroup'
        # group of the menubar.
        self.assertEqual(2, len(menu_manager.groups))

        ids = [group.id for group in menu_manager.groups]
        self.assertEqual(['FileMenuGroup', 'additions'], ids)

        group = menu_manager.find_group('FileMenuGroup')
        self.assertEqual('File', group.items[0].id)

        return

    def test_sub_menus_no_groups(self):
        """ sub-menus no groups """

        # We split the contributions into different action sets just because
        # that is how it might end up in an actual application... not because
        # you *have* to split them up this way!
        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', path='MenuBar'),
                    Menu(name='&Edit', path='MenuBar'),
                    Menu(name='&Tools', path='MenuBar'),
                    Menu(name='&Help', path='MenuBar')
                ],
            ),
        
            ActionSet(
                menus = [
                    Menu(name='&New', path='MenuBar/File'),
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        additions = menu.find_group('additions')

        self.assertEqual('New', additions.items[0].id)

        return

    def test_actions_no_groups(self):
        """ actions no groups """

        # We split the contributions into different action sets just because
        # that is how it might end up in an actual application... not because
        # you *have* to split them up this way!
        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', path='MenuBar'),
                    Menu(name='&Edit', path='MenuBar'),
                    Menu(name='&Tools', path='MenuBar'),
                    Menu(name='&Help', path='MenuBar')
                ]
            ),

            ActionSet(
                actions = [
                    Action(class_name='Exit', path='MenuBar/File'),
                    Action(class_name='About', path='MenuBar/Help')
                ]
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure the 'ExitAction' action got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        additions = menu.find_group('additions')

        self.assertEqual('Exit', additions.items[0].id)

        # Make sure the 'AboutAction' action got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item('Help')
        additions = menu.find_group('additions')

        self.assertEqual('About', additions.items[0].id)

        return

    def test_actions_make_submenus(self):
        """ actions make submenus """

        action_sets = [
            ActionSet(
                actions = [
                    Action(class_name='Folder', path='MenuBar/File/New'),
                    Action(class_name='File', path='MenuBar/File/New')
                ]
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure the 'File' menu got added to the 'additions' group of the
        # menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group('additions')
        self.assertEqual('File', additions.items[0].id)

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        additions = menu.find_group('additions')

        self.assertEqual('New', additions.items[0].id)

        # Make sure the new 'Folder' and 'File' actions got added to the
        # 'additions' group of the 'New' menu.
        menu = menu_manager.find_item('File/New')
        additions = menu.find_group('additions')

        self.assertEqual('Folder', additions.items[0].id)
        self.assertEqual('File', additions.items[1].id)

        return

    def test_actions_make_submenus_before_and_after(self):
        """ actions make submenus before and after """

        action_sets = [
            ActionSet(
                actions = [
                    Action(
                        class_name = 'File',
                        path       = 'MenuBar/File/New'
                    ),

                    Action(
                        class_name = 'Folder',
                        path       = 'MenuBar/File/New',
                        before     = 'File'
                    ),
                ]
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure the 'File' menu got added to the 'additions' group of the
        # menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group('additions')
        self.assertEqual('File', additions.items[0].id)

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        additions = menu.find_group('additions')

        self.assertEqual('New', additions.items[0].id)

        # Make sure the new 'Folder' and 'File' actions got added to the
        # 'additions' group of the 'New' menu.
        menu = menu_manager.find_item('File/New')
        additions = menu.find_group('additions')

        self.assertEqual('Folder', additions.items[0].id)
        self.assertEqual('File', additions.items[1].id)

        return

    def test_actions_and_menus_in_groups(self):
        """ actions and menus in groups """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(
                        name   = '&File',
                        path   = 'MenuBar',
                        groups = ['NewGroup', 'ExitGroup']
                    ),

                    Menu(name='&Edit', path='MenuBar'),
                    Menu(name='&Tools', path='MenuBar'),
                    Menu(name='&Help', path='MenuBar')
                ],
            ),

            ActionSet(
                menus = [
                    Menu(name='&New', path='MenuBar/File', group='NewGroup'),
                ],
            ),

            ActionSet(
                actions = [
                    Action(
                        class_name = 'Exit',
                        path       = 'MenuBar/File',
                        group      = 'ExitGroup'
                    ),
                ]
            ),
            
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
##         menu_manager.dump()

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))

        additions = menu_manager.find_group('additions')
        ids = [item.id for item in additions.items]
        self.assertEqual(['File', 'Edit', 'Tools', 'Help'], ids)

        # Make sure the 'File' menu has got 3 groups, 'NewGroup', 'ExitGroup'
        # and 'additions' (and in that order!).
        menu = menu_manager.find_item('File')
        self.assertEqual(3, len(menu.groups))

        ids = [group.id for group in menu.groups]
        self.assertEqual(['NewGroup', 'ExitGroup', 'additions'], ids)
        
        # Make sure the 'New' sub-menu got added to the 'NewGroup' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        group = menu.find_group('NewGroup')

        self.assertEqual('New', group.items[0].id)

        # Make sure the 'Exit' action got added to the 'ExitGroup' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        group = menu.find_group('ExitGroup')

        self.assertEqual('Exit', group.items[0].id)

        return
    
#### EOF ######################################################################
