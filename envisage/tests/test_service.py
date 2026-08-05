# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the 'Service' trait type. """

# Standard library imports.
import unittest

# Enthought library imports.
from traits.api import HasTraits, Instance, List, TraitError

from envisage.api import (
    CorePlugin,
    Plugin,
    Service,
    SERVICE_OFFERS,
    ServiceOffer,
)
from envisage.tests.support import SimpleApplication


class ServiceTestCase(unittest.TestCase):
    """Tests for the 'Service' trait type."""

    def test_service_trait_type(self):
        """service trait type"""

        class Foo(HasTraits):
            pass

        class PluginA(Plugin):
            """A plugin that offers a service."""

            id = "A"

            foo = Instance(Foo, ())

            service_offers = List(contributes_to=SERVICE_OFFERS)

            def _service_offers_default(self):
                """Trait initializer."""

                return [ServiceOffer(protocol=Foo, factory=self._foo_factory)]

            def _foo_factory(self, **properties):
                """Service factory."""

                return self.foo

        class PluginB(Plugin):
            """A plugin that uses the service."""

            id = "B"

            foo = Service(Foo)

        a = PluginA()
        b = PluginB()

        application = SimpleApplication(plugins=[CorePlugin(), a, b])
        application.start()

        # The 'Service' trait finds the service that PluginA offers.
        self.assertEqual(b.foo, a.foo)

        # Stop the application.
        application.stop()

        # The 'Service' trait re-reads the registry, so the service has gone.
        self.assertIsNone(b.foo)

        # You can't set service traits!
        with self.assertRaises(TraitError):
            setattr(b, "foo", "bogus")

    def test_service_trait_type_with_no_service_registry(self):
        """service trait type with no service registry"""

        class Foo(HasTraits):
            pass

        class Bar(HasTraits):
            foo = Service(Foo)

        # We should get an exception because the object does not have an
        # 'service_registry' trait.
        b = Bar()
        with self.assertRaises(ValueError):
            getattr(b, "foo")

    def test_service_str_representation(self):
        """test the string representation of the service"""

        class Foo(HasTraits):
            pass

        service_repr = "Service(protocol={!r})"
        service = Service(Foo)
        self.assertEqual(service_repr.format(Foo), str(service))
        self.assertEqual(service_repr.format(Foo), repr(service))
