""" Tests for the preference service. """


# Standard library imports.
import os, unittest

# Enthought library imports.
from enthought.envisage.preferences.api import Preferences, PreferencesService


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

    def test_set_and_get(self):
        """ set and get """

        p = PreferencesService()

        # Try an empty path.
        self.failUnlessRaises(ValueError, p.get, '')
        self.failUnlessRaises(ValueError, p.set, '', 'a value')

        # Try non-existent names to get the default-default!
        self.assertEqual(None, p.get('bogus'))
        self.assertEqual(None, p.get('acme.bogus'))
        self.assertEqual(None, p.get('acme.ui.bogus'))

        # Try non-existent names to get a defined default.
        self.assertEqual('a value', p.get('bogus', 'a value'))
        self.assertEqual('a value', p.get('acme.bogus', 'a value'))
        self.assertEqual('a value', p.get('acme.ui.bogus', 'a value'))

        # Set some values.
        p.set('bgcolor', 'red')
        p.set('acme.bgcolor', 'green')
        p.set('acme.ui.bgcolor', 'blue')

        # Get them!
        self.assertEqual('red', p.get('bgcolor'))
        self.assertEqual('green', p.get('acme.bgcolor'))
        self.assertEqual('blue', p.get('acme.ui.bgcolor'))
        
        return

    def test_builtin_scopes(self):
        """ builtin scopes """

        p = PreferencesService()

        # Make sure the default built-in scopes get created.
        self.assertEqual(True, p.root.has_child('application'))
        self.assertEqual(True, p.root.has_child('default'))

        return

    def test_lookup_order(self):
        """ lookup order """

        p = PreferencesService()

        # Set a value in both the application and default scopes.
        p.set('application/acme.ui.bgcolor', 'red')
        p.set('default/acme.ui.bgcolor', 'yellow')

        # Make sure when we look it up we get the one in first scope in the
        # lookup order.
        self.assertEqual('red', p.get('acme.ui.bgcolor'))

        # But we can still get at each scope individually.
        #
        # fixme: This is what we have to do...
        application = p.root.node('application')
        self.assertEqual('red', application.get('acme.ui.bgcolor'))
        
        default = p.root.node('default') 
        self.assertEqual('yellow', default.get('acme.ui.bgcolor'))

        # fixme: But why shouldn't I be able to write this?
        #self.assertEqual('red', p.get('application/acme.ui.bgcolor'))
        #self.assertEqual('yellow', p.get('default/acme.ui.bgcolor'))

        return

    def test_save(self):
        """ save """

        p = PreferencesService()

        # Get the application scope.
        application = p.root.node('application')
        application.filename = 'test.ini'
        
        # Set a value.
        p.set('acme.ui.bgcolor', 'red')

        # Save all scopes.
        p.save()

        # Make sure a file was written.
        self.assertEqual(True, os.path.exists('test.ini'))

        # Load the 'ini' file into a new preferences node and make sure the
        # preference is in there.
        p = Preferences()
        p.load('test.ini')

        self.assertEqual('red', p.get('acme.ui.bgcolor'))

        # Cleanup.
        os.remove('test.ini')
        
        return

    def test_get_and_set_in_default_scope(self):
        """ set and get in default scope """

        p = PreferencesService()

        # Get the default scope.
        default = p.root.node('default')
        
        # Set a preference and make sure we can get it again!
        p.set('default/acme.ui.bgcolor', 'red')
        self.assertEqual('red', p.get('acme.ui.bgcolor'))
        self.assertEqual('red', default.get('acme.ui.bgcolor'))

        # Make sure it didn't go into the application scope.
        application = p.root.node('application')
        self.assertEqual(None, application.get('acme.ui.bgcolor'))
        self.assertEqual(None, p.get('acme.ui.bgcolor', nodes=[application]))

        return

    def test_get_and_set_in_application_scope(self):
        """ set and get in application scope """

        p = PreferencesService()

        # Get the application scope.
        application = p.root.node('application')
        
        # Set a preference and make sure we can get it again!
        p.set('application/acme.ui.bgcolor', 'red')
        self.assertEqual('red', p.get('acme.ui.bgcolor'))
        self.assertEqual('red', application.get('acme.ui.bgcolor'))

        # Make sure it didn't go into the default scope.
        default = p.root.node('default')
        self.assertEqual(None, default.get('acme.ui.bgcolor'))
        self.assertEqual(None, p.get('acme.ui.bgcolor', nodes=[default]))

        return

#### EOF ######################################################################
