""" Tests for the 'Preference' trait type. """


# Standard library imports.
import os, unittest

# Enthought library imports.
from enthought.envisage.preferences.api import Preference, Preferences
from enthought.traits.api import HasTraits, Int, Str


class PreferenceTestCase(unittest.TestCase):
    """ Tests for the 'Preference' trait type. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.preferences = Preference.preferences = Preferences()
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_preference(self):
        """ preference """

        class Widget(HasTraits):
            """ Some widget """

            # The preferences node that cotains our preferences.
            PREFERENCES = 'acme.widget'
            
            bgcolor = Preference(Str('black'))
            

        w = Widget()

        # There is currently no preference so we should get the default value.
        self.assertEqual('black', w.bgcolor)

        # Now set the preference.
        self.preferences.set('acme.widget.bgcolor', 'red')
        self.assertEqual('red', w.bgcolor)

        # Set the preference via the trait type.
        w.bgcolor = 'yellow'
        self.assertEqual('yellow', self.preferences.get('acme.widget.bgcolor'))

        self.preferences.dump()
        
        return
    
#### EOF ######################################################################
