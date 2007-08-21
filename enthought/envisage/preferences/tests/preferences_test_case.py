""" Tests for preferences. """


# Standard library imports.
import os, unittest

# Enthought library imports.
from enthought.envisage.preferences.api import Preferences
from enthought.traits.api import HasTraits, Int, Str


class PreferencesTestCase(unittest.TestCase):
    """ Tests for preferences. """

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

    def test_node(self):
        """ node """

        p = Preferences()

        # Try an empty path.
        self.failUnlessRaises(ValueError, p.node, '')

        # Try a simple path.
        node = p.node('acme')
        self.assertNotEqual(None, node)
        self.assertEqual('acme', node.name)
        self.assertEqual('acme', node.path)

        # Make sure we get the same node each time we ask for it!
        self.assertEqual(node, p.node('acme'))
        
        # Try a nested path.
        node = p.node('acme.ui')
        self.assertNotEqual(None, node)
        self.assertEqual('ui', node.name)
        self.assertEqual('acme.ui', node.path)

        return

    def test_set_and_get(self):
        """ set and get """

        p = Preferences()

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

    def test_keys(self):
        """ keys """

        p = Preferences()

        # Empty!
        self.assertEqual([], p.keys())

        # Simple path.
        p.set('a', '1')
        p.set('b', '2')
        p.set('c', '3')

        keys = p.keys()
        keys.sort()

        self.assertEqual(['a', 'b', 'c'], keys)

        # Nested path.
        p.set('acme.a', '1')
        p.set('acme.b', '2')
        p.set('acme.c', '3')

        keys = p.keys('acme')
        keys.sort()
        
        self.assertEqual(['a', 'b', 'c'], keys)

        return

    def test_load(self):
        """ load """

        p = Preferences()

        # Load the preferences from an 'ini' file.
        p.load('example.ini')

        # Make sure it was all loaded!
        self.assertEqual(
            'Acme Lab', p.get('acme.ui.workbench.application_name')
        )

        self.assertEqual(
            'application.ico', p.get('acme.ui.workbench.application_icon')
        )

        self.assertEqual(
            'splash', p.get('acme.ui.workbench.splash_screen.image')
        )

        self.assertEqual(
            '5', p.get('acme.ui.workbench.splash_screen.text_x')
        )

        self.assertEqual(
            '10', p.get('acme.ui.workbench.splash_screen.text_y')
        )

        self.assertEqual(
            'red', p.get('acme.ui.workbench.splash_screen.text_color')
        )

        return

    def test_save(self):
        """ save """

        p = Preferences()

        # Load the preferences from an 'ini' file.
        p.load('example.ini')

        # Save it to another file.
        p.save('tmp.ini')

        # Load it into a new context.
        p = Preferences()
        p.load('tmp.ini')
        
        # Make sure it was all loaded!
        self.assertEqual(
            'Acme Lab', p.get('acme.ui.workbench.application_name')
        )

        self.assertEqual(
            'application.ico', p.get('acme.ui.workbench.application_icon')
        )

        self.assertEqual(
            'splash', p.get('acme.ui.workbench.splash_screen.image')
        )

        self.assertEqual(
            '5', p.get('acme.ui.workbench.splash_screen.text_x')
        )

        self.assertEqual(
            '10', p.get('acme.ui.workbench.splash_screen.text_y')
        )

        self.assertEqual(
            'red', p.get('acme.ui.workbench.splash_screen.text_color')
        )

        # Clean up!
        os.remove('tmp.ini')

        return

    def test_has_child(self):
        """ has child """

        p = Preferences()
        self.assertEqual(False, p.has_child('acme'))

        p.node('acme')
        self.assertEqual(True, p.has_child('acme'))
        
        return
        
##     def test_preference_trait_type(self):
##         """ preference trait type """

##         class SplashScreen(HasTraits):
##             """ A splash screen. """
            
##             image  = Preference(Str, 'acme.splash_screen.image')
##             text_x = Preference(Int(5), 'acme.splash_screen.text_x')
##             text_y = Preference(Int(10), 'acme.splash_screen.text_y')

##         splash_screen = SplashScreen()
##         self.assertEqual('', splash_screen.image)
##         self.assertEqual(5, splash_screen.text_x)
##         self.assertEqual(10, splash_screen.text_y)
        
##         return
    
#### EOF ######################################################################
