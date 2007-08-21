""" Tests for the 'Preference' trait type. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.preferences.api import Preference, Preferences
from enthought.traits.api import Bool, Float, HasTraits, Int, Str


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

    def test_str_preference(self):
        """ str preferences """

        class Widget(HasTraits):
            """ Some widget """

            # The preferences node that contains our preferences.
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
        
        return

    def test_int_preference(self):
        """ int preference """

        class Widget(HasTraits):
            """ Some widget """

            # The preferences node that contains our preferences.
            PREFERENCES = 'acme.widget'

            width = Preference(Int(100))

        w = Widget()

        # There is currently no preference so we should get the default value.
        self.assertEqual(100, w.width)

        # Now set the preference via the preferences node.
        self.preferences.set('acme.widget.width', 50)
        self.assertEqual(50, w.width)
        self.assertEqual('50', self.preferences.get('acme.widget.width'))

        # Set the preference via the trait type.
        w.width = 200
        self.assertEqual(200, w.width)
        self.assertEqual('200', self.preferences.get('acme.widget.width'))

        return

    def test_float_preference(self):
        """ float preferences """

        class Widget(HasTraits):
            """ Some widget """

            # The preferences node that contains our preferences.
            PREFERENCES = 'acme.widget'

            ratio = Preference(Float(0.25))

        w = Widget()

        # There is currently no preference so we should get the default value.
        self.assertEqual(0.25, w.ratio)

        # Now set the preference via the preferences node.
        self.preferences.set('acme.widget.ratio', 0.5)
        self.assertEqual(0.5, w.ratio)
        self.assertEqual('0.5', self.preferences.get('acme.widget.ratio'))

        # Set the preference via the trait type.
        w.ratio = 1.5
        self.assertEqual(1.5, w.ratio)
        self.assertEqual('1.5', self.preferences.get('acme.widget.ratio'))
        
        return

    def test_bool_preference(self):
        """ bool preference """

        class Widget(HasTraits):
            """ Some widget """

            # The preferences node that contains our preferences.
            PREFERENCES = 'acme.widget'

            visible = Preference(Bool)

        w = Widget()

        # There is currently no preference so we should get the default value.
        self.assertEqual(False, w.visible)

        # Now set the preference via the preferences node.
        self.preferences.set('acme.widget.visible', True)
        self.assertEqual(True, w.visible)
        self.assertEqual('True', self.preferences.get('acme.widget.visible'))

        # Set the preference via the trait type.
        w.visible = False
        self.assertEqual(False, w.visible)
        self.assertEqual('False', self.preferences.get('acme.widget.visible'))
        
        return

    def test_explicit_path(self):
        """ explicit path """

        class Widget(HasTraits):
            """ Some widget """

            # The preferences node that contains our preferences.
            PREFERENCES = 'acme.widget'
            
            bgcolor = Preference(Str('black'), PREFERENCES + '.bg')
            

        w = Widget()

        # There is currently no preference so we should get the default value.
        self.assertEqual('black', w.bgcolor)

        # Now set the preference.
        self.preferences.set('acme.widget.bg', 'red')
        self.assertEqual('red', w.bgcolor)

        # Set the preference via the trait type.
        w.bgcolor = 'yellow'
        self.assertEqual('yellow', self.preferences.get('acme.widget.bg'))
        
        return
    
#### EOF ######################################################################
