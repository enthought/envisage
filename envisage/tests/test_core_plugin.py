# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the core plugin. """


# Major package imports.
from pkg_resources import resource_filename

# Enthought library imports.
from envisage.api import Application, Category, ClassLoadHook, Plugin
from envisage.api import ServiceOffer
from traits.api import HasTraits, Int, Interface, List
from traits.testing.unittest_tools import unittest


# This module's package.
PKG = 'envisage.tests'


class TestApplication(Application):
    """ The type of application used in the tests. """

    id = 'core.plugin.test'


class CorePluginTestCase(unittest.TestCase):
    """ Tests for the core plugin. """

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

    def test_dynamically_added_service_offer(self):
        """ dynamically added service offer """

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

        # Start off with just the core plugin.
        application = TestApplication(plugins=[core])
        application.start()

        # Make sure the service does not exist!
        service = application.get_service(IMyService)
        self.assertIsNone(service)

        # Make sure the service offer exists...
        extensions = application.get_extensions('envisage.service_offers')
        self.assertEqual(0, len(extensions))

        # Now add a plugin that contains a service offer.
        application.add_plugin(a)

        # Make sure the service offer exists...
        extensions = application.get_extensions('envisage.service_offers')
        self.assertEqual(1, len(extensions))

        # ... and that the core plugin responded to the new service offer and
        # published it in the service registry.
        service = application.get_service(IMyService)
        self.assertEqual(42, service)

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
        self.assertTrue('y' in Bar.class_traits())

    def test_dynamically_added_category(self):
        """ dynamically added category """

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

        # Start with just the core plugin.
        application = TestApplication(plugins=[core])
        application.start()

        # Now add a plugin that contains a category.
        application.add_plugin(a)

        # Create the target class.
        class Bar(HasTraits):
            x = Int

        # Make sure the category was imported and added.
        self.assertTrue('y' in Bar.class_traits())

    def test_class_load_hooks(self):
        """ class load hooks """

        from envisage.core_plugin import CorePlugin

        def on_class_loaded(cls):
            """ Called when a class has been loaded. """

            on_class_loaded.cls = cls

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
        self.assertTrue(not hasattr(on_class_loaded, 'cls'))

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

    def test_dynamically_added_class_load_hooks(self):
        """ dynamically class load hooks """

        from envisage.core_plugin import CorePlugin

        def on_class_loaded(cls):
            """ Called when a class has been loaded. """

            on_class_loaded.cls = cls


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

        # Start with just the core plugin.
        application = TestApplication(plugins=[core])
        application.start()

        # Now add a plugin that contains a class load hook.
        application.add_plugin(a)

        # Make sure we ignore a class that we are not interested in!
        class Bif(HasTraits):
            pass

        # Make sure the class load hook was *ignored*.
        self.assertTrue(not hasattr(on_class_loaded, 'cls'))

        # Create the target class.
        class Baz(HasTraits):
            pass

        # Make sure the class load hook was called.
        self.assertEqual(Baz, on_class_loaded.cls)

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


        core = CorePlugin()
        a    = PluginA()

        application = TestApplication(plugins=[core, a])
        application.run()

        # Make sure we can get one of the preferences.
        self.assertEqual('42', application.preferences.get('enthought.test.x'))

    def test_dynamically_added_preferences(self):
        """ dynamically added preferences """

        # The core plugin is the plugin that offers the preferences extension
        # point.
        from envisage.core_plugin import CorePlugin

        class PluginA(Plugin):
            id = 'A'
            preferences = List(contributes_to='envisage.preferences')

            def _preferences_default(self):
                """ Trait initializer. """

                return ['file://' + resource_filename(PKG, 'preferences.ini')]

        core = CorePlugin()
        a    = PluginA()

        # Start with just the core plugin.
        application = TestApplication(plugins=[core])
        application.start()

        # Now add a plugin that contains a preference.
        application.add_plugin(a)

        # Make sure we can get one of the preferences.
        self.assertEqual('42', application.preferences.get('enthought.test.x'))
