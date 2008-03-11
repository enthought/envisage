""" Tests for the core plugin. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Application, Category, ClassLoadHook, Plugin
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

    def test_class_load_hooks(self):
        """ class load hooks """

        from enthought.envisage.core_plugin import CorePlugin

        def on_class_loaded(cls):
            """ Called when a class has been loaded. """

            on_class_loaded.cls = cls

            return

        class PluginA(Plugin):
            id = 'A'

            class_load_hooks = List(
                [
                    ClassLoadHook(
                        class_name = 'core_plugin_test_case.Baz',
                        on_load    = on_class_loaded,
                    )
                ],
                
                extension_point='enthought.envisage.class_load_hooks'
            )

        core = CorePlugin()
        a    = PluginA()
        
        application = TestApplication(plugins=[core, a])
        application.start()

        # Make sure we ignore a class that we are not interested in!
        class Bif(HasTraits):
            pass

        # Make sure the class load hook was *ignored*.
        self.assert_(not hasattr(on_class_loaded, 'cls'))
        
        # Create the target class.
        class Baz(HasTraits):
            pass
 
        # Make sure the class load hook was called.
        self.assertEqual(Baz, on_class_loaded.cls)
       
        return

    def test_preferences(self):
        """ preferences """

        from enthought.envisage.core_plugin import CorePlugin
        
        class PluginA(Plugin):
            id = 'A'

            preferences = List(
                ['file://preferences.ini'], 
                extension_point='enthought.envisage.preferences'
            )

        core = CorePlugin()
        a    = PluginA()
        
        application = TestApplication(plugins=[core, a])
        application.start()

        # Make sure the preferences file was loaded.
        x = application.preferences.get('enthought.test.x')
        self.assertEqual('42', x)
        
        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
