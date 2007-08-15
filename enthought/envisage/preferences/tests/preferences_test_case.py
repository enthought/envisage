""" Tests for applications. """


# Standard library imports.
import unittest

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

    def test_preferences(self):
        """ preferences """

        p = Preferences()
        p.dump()
        
        #p.node('enthought')
        #p.dump()

        #p.node('enthought.envisage.ui.workbench')
        #p.dump()

        #p.node('airbus.aerocity.ui.workbench')
        #p.dump()

        #p.set('enthought.envisage.ui.workbench.bgcolor', 'Blue')
        #p.dump()

        #print p.get('enthought.envisage.ui.workbench.bgcolor')


        #print p.keys('enthought.envisage.ui.workbench')
        #print p.keys('enthought.envisage.ui.workbench.bgcolor')


        p.load('example.ini')
        p.dump()
        
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
