""" Tests for the preference helper. """


# Standard library imports.
import os, unittest

# Enthought library imports.
from enthought.envisage.preferences.api import Preferences, PreferencesHelper
from enthought.traits.api import CInt, Str


class PreferencesHelperTestCase(unittest.TestCase):
    """ Tests for the preference helper. """

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

    def test_helper(self):
        """ helper """

        preferences = Preferences()
        preferences.load('example.ini')

        class SplashScreenPreferencesHelper(PreferencesHelper):
            """ A helper! """

            # Thepath to the preferences node.
            path = 'acme.ui.workbench.splash_screen'

            # The traits that we want to initialize from preferences.
            image      = Str
            text_x     = CInt
            text_y     = CInt
            text_color = Str
            
        helper = SplashScreenPreferencesHelper(preferences=preferences)

        self.assertEqual('splash', helper.image)
        self.assertEqual(5, helper.text_x)
        self.assertEqual(10, helper.text_y)
        self.assertEqual('red', helper.text_color)

        return

#### EOF ######################################################################
