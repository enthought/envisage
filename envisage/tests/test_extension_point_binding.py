# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for extension point bindings. """

# Standard library imports.
import unittest
import weakref

from traits.api import Any, HasTraits, List

# Enthought library imports.
from envisage.api import (
    bind_extension_point,
    ExtensionPoint,
    unbind_extension_point,
)

# Local imports.
from envisage.tests.mutable_extension_registry import MutableExtensionRegistry


class BindingTarget(HasTraits):
    """
    Example class whose traits are used as a binding target.
    """

    #: Target trait for extension point binding.
    target = List(Any())


class ExtensionPointBindingTestCase(unittest.TestCase):
    """Tests for extension point binding."""

    def setUp(self):
        self.extension_registry = MutableExtensionRegistry()

    def tearDown(self):
        del self.extension_registry

    def test_untyped_extension_point(self):
        """untyped extension point"""

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Add an extension.
        registry.add_extension("my.ep", 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        events = []
        f = Foo()
        f.observe(events.append, "x_items")

        # Make some bindings.
        bind_extension_point(f, "x", "my.ep", registry)

        # Make sure that the object was initialized properly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Add another extension.
        registry.add_extension("my.ep", "a string")

        # Make sure that the object picked up the new extension...
        self.assertEqual(2, len(f.x))
        self.assertTrue(42 in f.x)
        self.assertTrue("a string" in f.x)

        # ... and that the correct trait change event was fired.
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(f, event.object)
        self.assertEqual("x_items", event.name)
        self.assertEqual(1, len(event.new.added))
        self.assertTrue("a string" in event.new.added)

    def test_set_extensions_via_trait(self):
        """set extensions via trait"""

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Add an extension.
        registry.add_extension("my.ep", 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        events = []
        f = Foo()
        f.observe(events.append, "*")

        # Make some bindings.
        bind_extension_point(f, "x", "my.ep", registry)

        # Make sure that the object was initialized properly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Set the extensions.
        f.x = ["a string"]

        # Make sure that the object picked up the new extension...
        self.assertEqual(1, len(f.x))
        self.assertTrue("a string" in f.x)

        self.assertEqual(1, len(registry.get_extensions("my.ep")))
        self.assertTrue("a string" in registry.get_extensions("my.ep"))

        # ... and that the correct trait change event was fired.
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(f, event.object)
        self.assertEqual("x", event.name)
        self.assertEqual(1, len(event.new))
        self.assertTrue("a string" in event.new)

    def test_set_extensions_via_registry(self):
        """set extensions via registry"""

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Add an extension.
        registry.add_extension("my.ep", 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        events = []
        f = Foo()
        f.observe(events.append, "*")

        # Make some bindings.
        bind_extension_point(f, "x", "my.ep", registry)

        # Make sure that the object was initialized properly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(42, f.x[0])

        # Set the extensions.
        registry.set_extensions("my.ep", ["a string"])

        # Make sure that the object picked up the new extension...
        self.assertEqual(1, len(f.x))
        self.assertTrue("a string" in f.x)

        # ... and that the correct trait change event was fired.
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(f, event.object)
        self.assertEqual("x", event.name)
        self.assertEqual(1, len(event.new))
        self.assertTrue("a string" in event.new)

    def test_explicit_extension_registry(self):
        """explicit extension registry"""

        registry = self.extension_registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # Add an extension.
        registry.add_extension("my.ep", 42)

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = List

        f = Foo()

        # Create an empty extension registry use that in the binding.
        extension_registry = MutableExtensionRegistry()

        # Make some bindings.
        bind_extension_point(f, "x", "my.ep", extension_registry)

        # Make sure that we pick up the empty extension registry and not the
        # default one.
        self.assertEqual(0, len(f.x))

    def test_should_be_able_to_bind_multiple_traits_on_a_single_object(self):
        registry = self.extension_registry

        # Add 2 extension points.
        registry.add_extension_point(self._create_extension_point("my.ep"))
        registry.add_extension_point(
            self._create_extension_point("another.ep")
        )

        # Declare a class that consumes both of the extension points.
        class Foo(HasTraits):
            x = List
            y = List

        f = Foo()

        # Bind two different traits on the object to the extension points.
        bind_extension_point(f, "x", "my.ep", registry)
        bind_extension_point(f, "y", "another.ep", registry)
        self.assertEqual(0, len(f.x))
        self.assertEqual(0, len(f.y))

        # Add some contributions to the extension points.
        registry.add_extension("my.ep", 42)
        registry.add_extensions("another.ep", [98, 99, 100])

        # Make sure both traits were bound correctly.
        self.assertEqual(1, len(f.x))
        self.assertEqual(3, len(f.y))

    def test_unbind_extension_point(self):
        # Given ...
        # ... an extension point ...
        registry = self.extension_registry
        registry.add_extension_point(self._create_extension_point("my.ep"))

        # ... and an object with a corresponding trait ...
        target = BindingTarget()

        # When we bind the extension point to the trait ...
        bind_extension_point(target, "target", "my.ep", registry)

        # Then contributions to the extension point modify the trait.
        registry.add_extension("my.ep", "a string")
        self.assertEqual(target.target, ["a string"])

        # When we unbind the extension point
        unbind_extension_point(target, "target", "my.ep", registry)

        # Then contributions no longer change the trait.
        registry.add_extension("my.ep", "another string")
        self.assertEqual(target.target, ["a string"])

    def test_unbinding_removes_references(self):
        # Given an extension point bound to a trait
        extension_point = self._create_extension_point("my.ep")
        self.extension_registry.add_extension_point(extension_point)
        target = BindingTarget()
        bind_extension_point(
            target, "target", "my.ep", self.extension_registry
        )

        # Use a weakref finalizer to keep track of whether 'target' still
        # has references keeping it alive.
        target_monitor = weakref.finalize(target, lambda: None)

        # When we unbind and delete the target object
        unbind_extension_point(
            target, "target", "my.ep", self.extension_registry
        )
        del target

        # Then 'target' should no longer be alive.
        self.assertFalse(target_monitor.alive)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=""):
        """Create an extension point."""

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc)
