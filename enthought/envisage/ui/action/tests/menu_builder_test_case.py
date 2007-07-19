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

    def _create_action(self, action_extension):
        """ Creates an action implementation from an action extension. """

        from enthought.pyface.action.api import Action
        return Action(name=action_extension.class_name)

    def _create_group(self, group_extension):
        """ Creates a group implementation from a group extension. """

        from enthought.pyface.action.api import Group
        return Group(id=group_extension.id)

    def _create_menu_manager(self, menu_extension):
        """ Creates a menu manager implementation from a menu extension. """

        from enthought.pyface.action.api import MenuManager
        return MenuManager(id=menu_extension.id)

    
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

    def test_top_level_menus_with_no_groups(self):
        """ top level menus with no groups """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', location='MenuBar'),
                    Menu(name='&Edit', location='MenuBar'),
                    Menu(name='&Tools', location='MenuBar'),
                    Menu(name='&Help', location='MenuBar')
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
        menu_manager.dump()

        # Make sure that all of the menus were added the the 'additions' group
        # of the menubar.
        self.assertEqual(1, len(menu_manager.groups))
        self.assertEqual('additions', menu_manager.groups[0].id)

        additions = menu_manager.groups[0]
        self.assertEqual('File', additions.items[0].id)
        self.assertEqual('Edit', additions.items[1].id)
        self.assertEqual('Tools', additions.items[2].id)
        self.assertEqual('Help', additions.items[3].id)

        return

    def test_sub_menus_with_no_groups(self):
        """ sub-menus with no groups """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', location='MenuBar'),
                    Menu(name='&Edit', location='MenuBar'),
                    Menu(name='&Tools', location='MenuBar'),
                    Menu(name='&Help', location='MenuBar')
                ],
            
                actions = [
                    Action(class_name='Exit', locations=['MenuBar/File']),
                    Action(class_name='About', locations=['MenuBar/Help'])
                ]
            ),
        
            ActionSet(
                menus = [
                    Menu(name='&New',  location='MenuBar/File'),
                ],
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
        menu_manager.dump()

        # Make sure the 'New' sub-menu got added to the 'additions' group
        # of the 'File' menu.
        menu = menu_manager.find_item('File')
        additions = menu.find_group('additions')

        self.assertEqual('New', additions.items[0].id)

        return

    def test_actions_with_no_groups(self):
        """ actions with no groups """

        action_sets = [
            ActionSet(
                menus = [
                    Menu(name='&File', location='MenuBar'),
                    Menu(name='&Edit', location='MenuBar'),
                    Menu(name='&Tools', location='MenuBar'),
                    Menu(name='&Help', location='MenuBar')
                ],
            
                actions = [
                    Action(class_name='Exit', locations=['MenuBar/File']),
                    Action(class_name='About', locations=['MenuBar/Help'])
                ]
            )
        ]

        # Create a menu builder containing the action set.
        menu_builder = TestMenuBuilder(action_sets=action_sets)

        # Create a menu manager for the 'MenuBar'.
        menu_manager = menu_builder.create_menu_bar_manager('MenuBar')
        menu_manager.dump()

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
    
#### EOF ######################################################################
