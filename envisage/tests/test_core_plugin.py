# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the core plugin. """

# Standard library imports.
import unittest

# Major package imports.
from pkg_resources import resource_filename

from traits.api import HasTraits, Interface, List, on_trait_change, Str

# Enthought library imports.
from envisage.api import CorePlugin, Plugin, ServiceOffer
from envisage.tests.support import SimpleApplication

# This module's package.
PKG = "envisage.tests"


class CorePluginTestCase(unittest.TestCase):
    """Tests for the core plugin."""

    def test_service_offers(self):
        """service offers"""

        class IMyService(Interface):
            pass

        class PluginA(Plugin):
            id = "A"

            service_offers = List(contributes_to="envisage.service_offers")

            def _service_offers_default(self):
                """Trait initializer."""

                service_offers = [
                    ServiceOffer(
                        protocol=IMyService, factory=self._my_service_factory
                    )
                ]

                return service_offers

            def _my_service_factory(self, **properties):
                """Service factory."""

                return 42

        core = CorePlugin()
        a = PluginA()

        application = SimpleApplication(plugins=[core, a])
        application.start()

        # Lookup the service.
        self.assertEqual(42, application.get_service(IMyService))

        # Stop the core plugin.
        application.stop_plugin(core)

        # Make sure th service has gone.
        self.assertEqual(None, application.get_service(IMyService))

    def test_dynamically_added_service_offer(self):
        """dynamically added service offer"""

        class IMyService(Interface):
            pass

        class PluginA(Plugin):
            id = "A"

            service_offers = List(contributes_to="envisage.service_offers")

            def _service_offers_default(self):
                """Trait initializer."""

                service_offers = [
                    ServiceOffer(
                        protocol=IMyService, factory=self._my_service_factory
                    )
                ]

                return service_offers

            def _my_service_factory(self, **properties):
                """Service factory."""

                return 42

        core = CorePlugin()
        a = PluginA()

        # Start off with just the core plugin.
        application = SimpleApplication(plugins=[core])
        application.start()

        # Make sure the service does not exist!
        service = application.get_service(IMyService)
        self.assertIsNone(service)

        # Make sure the service offer exists...
        extensions = application.get_extensions("envisage.service_offers")
        self.assertEqual(0, len(extensions))

        # Now add a plugin that contains a service offer.
        application.add_plugin(a)

        # Make sure the service offer exists...
        extensions = application.get_extensions("envisage.service_offers")
        self.assertEqual(1, len(extensions))

        # ... and that the core plugin responded to the new service offer and
        # published it in the service registry.
        service = application.get_service(IMyService)
        self.assertEqual(42, service)

    def test_preferences(self):
        """preferences"""

        class PluginA(Plugin):
            id = "A"
            preferences = List(contributes_to="envisage.preferences")

            def _preferences_default(self):
                """Trait initializer."""

                return ["file://" + resource_filename(PKG, "preferences.ini")]

        core = CorePlugin()
        a = PluginA()

        application = SimpleApplication(plugins=[core, a])
        application.run()

        # Make sure we can get one of the preferences.
        self.assertEqual("42", application.preferences.get("enthought.test.x"))

    def test_dynamically_added_preferences(self):
        """dynamically added preferences"""

        class PluginA(Plugin):
            id = "A"
            preferences = List(contributes_to="envisage.preferences")

            def _preferences_default(self):
                """Trait initializer."""

                return ["file://" + resource_filename(PKG, "preferences.ini")]

        core = CorePlugin()
        a = PluginA()

        # Start with just the core plugin.
        application = SimpleApplication(plugins=[core])
        application.start()

        # Now add a plugin that contains a preference.
        application.add_plugin(a)

        # Make sure we can get one of the preferences.
        self.assertEqual("42", application.preferences.get("enthought.test.x"))

    # regression test for enthought/envisage#251
    def test_unregister_service_offer(self):
        """Unregister a service that is contributed to the
        "envisage.service_offers" extension point while the application is
        running.
        """

        class IJunk(Interface):
            trash = Str()

        class Junk(HasTraits):
            trash = Str("garbage")

        class PluginA(Plugin):
            # The Ids of the extension points that this plugin contributes to.
            SERVICE_OFFERS = "envisage.service_offers"

            service_offers = List(contributes_to=SERVICE_OFFERS)

            def _service_offers_default(self):
                a_service_offer = ServiceOffer(
                    protocol=IJunk,
                    factory=self._create_junk_service,
                )

                return [a_service_offer]

            def _create_junk_service(self):
                """Factory method for the 'Junk' service."""

                return Junk()

            @on_trait_change("application:started")
            def _unregister_junk_service(self):
                # only 1 service is registered so it has service_id of 1
                self.application.unregister_service(1)

        application = SimpleApplication(
            plugins=[CorePlugin(), PluginA()],
        )

        # Run it!
        application.run()

    def test_unregister_service(self):
        """Unregister a service which was registered on the application
        directly, not through the CorePlugin's extension point. CorePlugin
        should not do anything to interfere."""

        class IJunk(Interface):
            trash = Str()

        class Junk(HasTraits):
            trash = Str("garbage")

        some_junk = Junk()

        application = SimpleApplication(
            plugins=[CorePlugin()],
        )

        application.start()

        some_junk_id = application.register_service(IJunk, some_junk)
        application.unregister_service(some_junk_id)

        application.stop()
