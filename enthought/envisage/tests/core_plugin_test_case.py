""" Tests for the core plugin. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Application, Category, Plugin
from enthought.traits.api import HasTraits, Int, List


class TestApplication(Application):
    """ The type of application used in the tests. """

    id = 'core.plugin.test'

    
class CorePluginTestCase(unittest.TestCase):
    """ Tests for the core plugin. """

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

    def test_categories(self):
        """ categories """

        from enthought.envisage.core_plugin import CorePlugin
        
        class PluginA(Plugin):
            id = 'A'

            categories = List(
                [
                    Category(
                        class_name = 'bar_category.BarCategory',
                        target_class_name = 'core_plugin_test_case.Bar'
                    )
                ],
                
                extension_point='enthought.envisage.categories'
            )

        core = CorePlugin()
        a    = PluginA()
        
        application = TestApplication(plugins=[core, a])
        application.start()

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
