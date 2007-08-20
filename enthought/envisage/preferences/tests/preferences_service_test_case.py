""" Tests for the preference service. """


# Standard library imports.
import os, unittest

# Enthought library imports.
from enthought.envisage.preferences.api import PreferencesService


class PreferencesServiceTestCase(unittest.TestCase):
    """ Tests for the preference service. """

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

    def test_builtin_scopes(self):
        """ builtin scopes """

        ps = PreferencesService()

        # Make sure the default built-in scopes get created.
        self.assertEqual(True, ps.root.has_child('application'))
        self.assertEqual(True, ps.root.has_child('default'))

        return

    def test_set_in_default_scope(self):
        """ set in default scope """

        ps = PreferencesService()

        # Get the default scope.
        default = ps.root.node('default')
        
        # Set a preference and make sure we can get it again!
        default.set('acme.ui.bgcolor', 'red')
        self.assertEqual('red', ps.get('acme.ui.bgcolor'))

        # Make sure it didn't go into the application scope.
        application = ps.root.node('application')
        self.assertEqual(None, application.get('acme.ui.bgcolor'))
        self.assertEqual(None, ps.get('acme.ui.bgcolor', nodes=[application]))

        return

#### EOF ######################################################################
