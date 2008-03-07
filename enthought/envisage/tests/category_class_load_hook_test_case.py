""" Tests for category class load hooks. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.traits.api import HasTraits, Int

# fixme: Should these be in the api?
from enthought.envisage.category_class_load_hook import CategoryClassLoadHook


class CategoryClassLoadHookTestCase(unittest.TestCase):
    """ Tests for category class load hooks. """

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

    def test_category_class_load_hook(self):
        """ category class load hook """

        hook = CategoryClassLoadHook(
            class_name = 'category_class_load_hook_test_case.Bar',
            category_class_name = 'bar_category.BarCategory'
        )
        hook.connect()
        
        # Create the target class.
        class Bar(HasTraits):
            x = Int

        # Make sure the category was imported and added.
        self.assert_('y' in Bar.class_traits())
        
        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()
    
#### EOF ######################################################################
