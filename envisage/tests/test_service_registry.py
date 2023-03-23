# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the service registry. """


# Standard library imports.
import sys
import unittest

from traits.api import HasTraits, Int, Interface, provides

# Enthought library imports.
from envisage.api import Application, NoSuchServiceError, ServiceRegistry

# This module's package.
PKG = "envisage.tests"


def service_factory(**properties):
    """A factory for foos."""

    return HasTraits(**properties)


class ServiceRegistryTestCase(unittest.TestCase):
    """Tests for the service registry."""

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """Prepares the test fixture before each test method is called."""

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.service_registry = Application(service_registry=ServiceRegistry())

        # module 'foo' need to be cleared out when this test is run,
        # because other tests also import foo.
        if PKG + ".foo" in sys.modules:
            del sys.modules[PKG + ".foo"]

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_should_get_required_service(self):
        class Foo(HasTraits):
            price = Int

        foo = Foo()

        # Register a service factory.
        self.service_registry.register_service(Foo, foo)

        service = self.service_registry.get_required_service(Foo)
        self.assertIs(foo, service)

    def test_should_get_exception_if_required_service_is_missing(self):
        class IFoo(Interface):
            price = Int

        with self.assertRaises(NoSuchServiceError):
            self.service_registry.get_required_service(IFoo)

    def test_imported_service_factory(self):
        """imported service factory"""

        class IFoo(Interface):
            price = Int

        # Register a service factory.
        self.service_registry.register_service(
            HasTraits,
            PKG + ".test_service_registry.service_factory",
            {"price": 100},
        )

        # Create a query that matches the registered object.
        service = self.service_registry.get_service(HasTraits, "price <= 100")
        self.assertNotEqual(None, service)
        self.assertEqual(HasTraits, type(service))

        # This shows that the properties were passed in to the factory.
        self.assertEqual(100, service.price)

        # Make sure that the object created by the factory is cached (i.e. we
        # get the same object back from now on!).
        service2 = self.service_registry.get_service(HasTraits, "price <= 100")
        self.assertTrue(service is service2)

    def test_function_service_factory(self):
        """function service factory"""

        class IFoo(Interface):
            price = Int

        @provides(IFoo)
        class Foo(HasTraits):
            price = Int

        def foo_factory(**properties):
            """A factory for foos."""

            return Foo(**properties)

        # Register a service factory.
        self.service_registry.register_service(
            IFoo, foo_factory, {"price": 100}
        )

        # Create a query that matches the registered object.
        service = self.service_registry.get_service(IFoo, "price <= 100")
        self.assertNotEqual(None, service)
        self.assertEqual(Foo, type(service))

        # Make sure that the object created by the factory is cached (i.e. we
        # get the same object back from now on!).
        service2 = self.service_registry.get_service(IFoo, "price <= 100")
        self.assertTrue(service is service2)

    def test_lazy_function_service_factory(self):
        """lazy function service factory"""

        # Register a service factory by name.
        def foo_factory(**properties):
            """A factory for foos."""

            from envisage.tests.foo import Foo

            foo_factory.foo = Foo()

            return foo_factory.foo

        i_foo = PKG + ".i_foo.IFoo"
        foo = PKG + ".foo"

        self.service_registry.register_service(i_foo, foo_factory)

        # Get rid of the 'foo' module (used in other tests).
        if foo in sys.modules:
            del sys.modules[foo]

        # Make sure that we haven't imported the 'foo' module.
        self.assertTrue(foo not in sys.modules)

        # Look up a non-existent service.
        services = self.service_registry.get_services("bogus.IBogus")

        # Make sure that we *still* haven't imported the 'foo' module.
        self.assertTrue(foo not in sys.modules)

        # Look it up again.
        services = self.service_registry.get_services(i_foo)
        self.assertEqual([foo_factory.foo], services)
        self.assertTrue(foo in sys.modules)

        # Clean up!
        del sys.modules[foo]

    def test_lazy_bound_method_service_factory(self):
        """lazy bound method service factory"""

        i_foo = PKG + ".i_foo.IFoo"
        foo = PKG + ".foo"

        class ServiceProvider(HasTraits):
            """A class that provides a service.

            This is used to make sure a bound method can be used as a service
            factory.

            """

            # Register a service factory by name.
            def foo_factory(self, **properties):
                """A factory for foos."""

                from envisage.tests.foo import Foo

                self.foo = Foo()

                return self.foo

        sp = ServiceProvider()
        self.service_registry.register_service(i_foo, sp.foo_factory)

        # Get rid of the 'foo' module (used in other tests).
        if foo in sys.modules:
            del sys.modules[foo]

        # Make sure that we haven't imported the 'foo' module.
        self.assertTrue(foo not in sys.modules)

        # Look up a non-existent service.
        services = self.service_registry.get_services("bogus.IBogus")

        # Make sure that we *still* haven't imported the 'foo' module.
        self.assertTrue(foo not in sys.modules)

        # Look up the service.
        services = self.service_registry.get_services(i_foo)
        self.assertEqual([sp.foo], services)
        self.assertTrue(foo in sys.modules)

        # Clean up!
        del sys.modules[foo]

    def test_get_services(self):
        """get services"""

        class IFoo(Interface):
            pass

        @provides(IFoo)
        class Foo(HasTraits):
            pass

        # Register two services.
        foo = Foo()
        self.service_registry.register_service(IFoo, foo)

        foo = Foo()
        self.service_registry.register_service(IFoo, foo)

        # Look it up again.
        services = self.service_registry.get_services(IFoo)
        self.assertEqual(2, len(services))

        class IBar(Interface):
            pass

        # Lookup a non-existent service.
        services = self.service_registry.get_services(IBar)
        self.assertEqual([], services)

    def test_get_services_with_strings(self):
        """get services with strings"""

        from envisage.tests.foo import Foo

        # Register a couple of services using a string protocol name.
        protocol_name = "envisage.tests.foo.IFoo"

        self.service_registry.register_service(protocol_name, Foo())
        self.service_registry.register_service(protocol_name, Foo())

        # Look them up using the same string!
        services = self.service_registry.get_services(protocol_name)
        self.assertEqual(2, len(services))

    def test_get_services_with_query(self):
        """get services with query"""

        class IFoo(Interface):
            price = Int

        @provides(IFoo)
        class Foo(HasTraits):
            price = Int

        # Register two services.
        #
        # This one shows how the object's attributes are used when evaluating
        # a query.
        foo = Foo(price=100)
        self.service_registry.register_service(IFoo, foo)

        # This one shows how properties can be specified that *take precedence*
        # over the object's attributes when evaluating a query.
        goo = Foo(price=10)
        self.service_registry.register_service(IFoo, goo, {"price": 200})

        # Create a query that doesn't match any registered object.
        services = self.service_registry.get_services(IFoo, 'color == "red"')
        self.assertEqual([], services)

        # Create a query that matches one of the registered objects.
        services = self.service_registry.get_services(IFoo, "price <= 100")
        self.assertEqual([foo], services)

        # Create a query that matches both registered objects.
        services = self.service_registry.get_services(IFoo, "price >= 100")
        self.assertTrue(foo in services)
        self.assertTrue(goo in services)
        self.assertEqual(2, len(services))

        class IBar(Interface):
            pass

        # Lookup a non-existent service.
        services = self.service_registry.get_services(IBar, "price <= 100")
        self.assertEqual([], services)

    def test_get_service(self):
        """get service"""

        class IFoo(Interface):
            pass

        @provides(IFoo)
        class Foo(HasTraits):
            pass

        # Register a couple of services.
        foo = Foo()
        self.service_registry.register_service(IFoo, foo)

        goo = Foo()
        self.service_registry.register_service(IFoo, goo)

        # Look up one of them!
        service = self.service_registry.get_service(IFoo)
        self.assertTrue(foo is service or goo is service)

        class IBar(Interface):
            pass

        # Lookup a non-existent service.
        service = self.service_registry.get_service(IBar)
        self.assertEqual(None, service)

    def test_get_service_with_query(self):
        """get service with query"""

        class IFoo(Interface):
            price = Int

        @provides(IFoo)
        class Foo(HasTraits):
            price = Int

        # Register two services.
        #
        # This one shows how the object's attributes are used when evaluating
        # a query.
        foo = Foo(price=100)
        self.service_registry.register_service(IFoo, foo)

        # This one shows how properties can be specified that *take precedence*
        # over the object's attributes when evaluating a query.
        goo = Foo(price=10)
        self.service_registry.register_service(IFoo, goo, {"price": 200})

        # Create a query that doesn't match any registered object.
        service = self.service_registry.get_service(IFoo, "price < 100")
        self.assertEqual(None, service)

        # Create a query that matches one of the registered objects.
        service = self.service_registry.get_service(IFoo, "price <= 100")
        self.assertEqual(foo, service)

        # Create a query that matches both registered objects.
        service = self.service_registry.get_service(IFoo, "price >= 100")
        self.assertTrue(foo is service or goo is service)

        class IBar(Interface):
            pass

        # Lookup a non-existent service.
        service = self.service_registry.get_service(IBar, "price <= 100")
        self.assertEqual(None, service)

    def test_get_and_set_service_properties(self):
        """get and set service properties"""

        class IFoo(Interface):
            price = Int

        @provides(IFoo)
        class Foo(HasTraits):
            price = Int

        # Register two services.
        #
        # This one has no properties.
        foo = Foo(price=100)
        foo_id = self.service_registry.register_service(IFoo, foo)

        # This one has properties.
        goo = Foo(price=10)
        goo_id = self.service_registry.register_service(
            IFoo, goo, {"price": 200}
        )

        # Get the properties.
        foo_properties = self.service_registry.get_service_properties(foo_id)
        self.assertEqual({}, foo_properties)

        goo_properties = self.service_registry.get_service_properties(goo_id)
        self.assertEqual(200, goo_properties["price"])

        # Update the properties.
        foo_properties["price"] = 300
        goo_properties["price"] = 500

        # Set the properties.
        self.service_registry.set_service_properties(foo_id, foo_properties)
        self.service_registry.set_service_properties(goo_id, goo_properties)

        # Get the properties again.
        foo_properties = self.service_registry.get_service_properties(foo_id)
        self.assertEqual(300, foo_properties["price"])

        goo_properties = self.service_registry.get_service_properties(goo_id)
        self.assertEqual(500, goo_properties["price"])

        # Try to get the properties of a non-existent service.
        with self.assertRaises(ValueError):
            self.service_registry.get_service_properties(-1)

        # Try to set the properties of a non-existent service.
        with self.assertRaises(ValueError):
            self.service_registry.set_service_properties(-1, {})

    def test_unregister_service(self):
        """unregister service"""

        class IFoo(Interface):
            price = Int

        @provides(IFoo)
        class Foo(HasTraits):
            price = Int

        # Register two services.
        #
        # This one shows how the object's attributes are used when evaluating
        # a query.
        foo = Foo(price=100)
        foo_id = self.service_registry.register_service(IFoo, foo)

        # This one shows how properties can be specified that *take precedence*
        # over the object's attributes when evaluating a query.
        goo = Foo(price=10)
        goo_id = self.service_registry.register_service(
            IFoo, goo, {"price": 200}
        )

        # Create a query that doesn't match any registered object.
        service = self.service_registry.get_service(IFoo, "price < 100")
        self.assertEqual(None, service)

        # Create a query that matches one of the registered objects.
        service = self.service_registry.get_service(IFoo, "price <= 100")
        self.assertEqual(foo, service)

        # Create a query that matches both registered objects.
        service = self.service_registry.get_service(IFoo, "price >= 100")
        self.assertTrue(foo is service or goo is service)

        #### Now do some unregistering! ####

        # Unregister 'foo'.
        self.service_registry.unregister_service(foo_id)

        # This query should no longer match any of the registered objects.
        service = self.service_registry.get_service(IFoo, "price <= 100")
        self.assertEqual(None, service)

        # Unregister 'goo'.
        self.service_registry.unregister_service(goo_id)

        # This query should no longer match any of the registered objects.
        service = self.service_registry.get_service(IFoo, "price >= 100")
        self.assertEqual(None, service)

        # Try to unregister a non-existent service.
        with self.assertRaises(ValueError):
            self.service_registry.unregister_service(-1)

    def test_minimize_and_maximize(self):
        """minimize and maximize"""

        class IFoo(Interface):
            price = Int

        @provides(IFoo)
        class Foo(HasTraits):
            price = Int

        # Register some objects with various prices.
        x = Foo(price=10)
        y = Foo(price=5)
        z = Foo(price=100)

        for foo in [x, y, z]:
            self.service_registry.register_service(IFoo, foo)

        # Find the service with the lowest price.
        service = self.service_registry.get_service(IFoo, minimize="price")
        self.assertNotEqual(None, service)
        self.assertEqual(Foo, type(service))
        self.assertEqual(y, service)

        # Find the service with the highest price.
        service = self.service_registry.get_service(IFoo, maximize="price")
        self.assertNotEqual(None, service)
        self.assertEqual(Foo, type(service))
        self.assertEqual(z, service)
