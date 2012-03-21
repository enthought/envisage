""" Tests for the core plugin. """


# Standard library imports.
import unittest

# Major package imports.
from pkg_resources import resource_filename

# Enthought library imports.
from envisage.api import Application, Category, ClassLoadHook, Plugin
from envisage.api import ServiceOffer
from traits.api import HasTraits, Int, Interface, List


# This module's package.
PKG = 'envisage.tests'


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

    def test_service_offers(self):
        """ service offers """

        from envisage.core_plugin import CorePlugin

        class IMyService(Interface):
            pass

        class PluginA(Plugin):
            id = 'A'

            service_offers = List(
                contributes_to='envisage.service_offers'
            )

            def _service_offers_default(self):
                """ Trait initializer. """

                service_offers = [
                    ServiceOffer(
                        protocol=IMyService, factory=self._my_service_factory
                    )
                ]

                return service_offers

            def _my_service_factory(self, **properties):
                """ Service factory. """

                return 42


        core = CorePlugin()
        a    = PluginA()

        application = TestApplication(plugins=[core, a])
        application.start()

        # Lookup the service.
        self.assertEqual(42, application.get_service(IMyService))

        # Stop the core plugin.
        application.stop_plugin(core)

        # Make sure th service has gone.
        self.assertEqual(None, application.get_service(IMyService))

        return

    def test_categories(self):
        """ categories """

        from envisage.core_plugin import CorePlugin

        class PluginA(Plugin):
            id = 'A'

            categories = List(contributes_to='envisage.categories')

            def _categories_default(self):
                """ Trait initializer. """

                bar_category = Category(
                    class_name = PKG + '.bar_category.BarCategory',
                    target_class_name = CorePluginTestCase.__module__ + '.Bar'
                )

                return [bar_category]


        core = CorePlugin()
        a    = PluginA()

        application = TestApplication(plugins=[core, a])
        application.start()

        # Create the target class.
        class Bar(HasTraits):
            x = Int

        # Make sure the category was imported and added.
        #
        # fixme: The following assertion was commented out. Please don't do
        # that! If a test fails we need to work out why - otherwise you have
        # just completely removed the benefits of having tests in the first
        # place! This test works for me on Python 2.4!
        self.assert_('y' in Bar.class_traits())

        return

    def test_class_load_hooks(self):
        """ class load hooks """

        from envisage.core_plugin import CorePlugin

        def on_class_loaded(cls):
            """ Called when a class has been loaded. """

            on_class_loaded.cls = cls

            return

        class PluginA(Plugin):
            id = 'A'

            class_load_hooks = List(
                [
                    ClassLoadHook(
                        class_name = CorePluginTestCase.__module__ + '.Baz',
                        on_load    = on_class_loaded,
                    )
                ],

                contributes_to='envisage.class_load_hooks'
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
        #
        # fixme: The following assertion was commented out. Please don't do
        # that! If a test fails we need to work out why - otherwise you have
        # just completely removed the benefits of having tests in the first
        # place! This test works for me on Python 2.4!
        self.assertEqual(Baz, on_class_loaded.cls)

        return

    def test_preferences(self):
        """ preferences """

        # The core plugin is the plugin that offers the preferences extension
        # point.
        from envisage.core_plugin import CorePlugin

        class PluginA(Plugin):
            id = 'A'
            preferences = List(contributes_to='envisage.preferences')

            def _preferences_default(self):
                """ Trait initializer. """

                return ['file://' + resource_filename(PKG, 'preferences.ini')]

        application = TestApplication(plugins=[CorePlugin(), PluginA()])
        application.run()

        # Make sure we can get one of the preferences.
        self.assertEqual('42', application.preferences.get('enthought.test.x'))

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
