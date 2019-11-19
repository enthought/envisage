# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for extension points. """


# Enthought library imports.
from envisage.api import Application, ExtensionPoint
from envisage.api import ExtensionRegistry
from traits.api import HasTraits, Int, List, TraitError
from traits.testing.unittest_tools import unittest


class TestBase(HasTraits):
    """ Base class for all test classes that use the 'ExtensionPoint' type. """

    extension_registry = None


class ExtensionPointTestCase(unittest.TestCase):
    """ Tests for extension points. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.registry = Application(extension_registry=ExtensionRegistry())

        # Set the extension registry used by the test classes.
        TestBase.extension_registry = self.registry

    def test_invalid_extension_point_type(self):
        """ invalid extension point type """

        # Extension points currently have to be 'List's of something! The
        # default is a list of anything.
        with self.assertRaises(TypeError):
            ExtensionPoint(Int, "my.ep")

    def test_no_reference_to_extension_registry(self):
        """ no reference to extension registry """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', 'xxx')

        # Declare a class that consumes the extension.
        class Foo(HasTraits):
            x = ExtensionPoint(List(Int), id='my.ep')

        # We should get an exception because the object does not have an
        # 'extension_registry' trait.
        f = Foo()
        with self.assertRaises(ValueError):
            getattr(f, "x")

    def test_extension_point_changed(self):
        """ extension point changed """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Declare a class that consumes the extension.
        class Foo(TestBase):
            x = ExtensionPoint(id='my.ep')

            def _x_changed(self):
                """ Static trait change handler. """

                self.x_changed_called = True

        f = Foo()

        # Connect the extension points on the object so that it can listen
        # for changes.
        ExtensionPoint.connect_extension_point_traits(f)

        # Set the extensions.
        registry.set_extensions('my.ep', [42, 'a string', True])

        # Make sure that instances of the class pick up the extensions.
        self.assertEqual(3, len(f.x))
        self.assertEqual([42, 'a string', True],  f.x)

        # Make sure the trait change handler was called.
        self.assertTrue(f.x_changed_called)

        # Reset the change handler flag.
        f.x_changed_called = False

        # Disconnect the extension points on the object.
        ExtensionPoint.disconnect_extension_point_traits(f)

        # Set the extensions.
        registry.set_extensions('my.ep', [98, 99, 100])

        # Make sure the trait change handler was *not* called.
        self.assertEqual(False, f.x_changed_called)

    def test_untyped_extension_point(self):
        """ untyped extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', [42, 'a string', True])

        # Declare a class that consumes the extension.
        class Foo(TestBase):
            x = ExtensionPoint(id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.assertEqual(3, len(f.x))
        self.assertEqual([42, 'a string', True],  f.x)

        g = Foo()
        self.assertEqual(3, len(g.x))
        self.assertEqual([42, 'a string', True],  g.x)

    def test_typed_extension_point(self):
        """ typed extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', [42, 43, 44])

        # Declare a class that consumes the extension.
        class Foo(TestBase):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that instances of the class pick up the extensions.
        f = Foo()
        self.assertEqual(3, len(f.x))
        self.assertEqual([42, 43, 44], f.x)

        g = Foo()
        self.assertEqual(3, len(g.x))
        self.assertEqual([42, 43, 44], g.x)

    def test_invalid_extension_point(self):
        """ invalid extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Set the extensions.
        registry.set_extensions('my.ep', 'xxx')

        # Declare a class that consumes the extension.
        class Foo(TestBase):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure we get a trait error because the type of the extension
        # doesn't match that of the extension point.
        f = Foo()
        with self.assertRaises(TraitError):
            getattr(f, "x")

    def test_extension_point_with_no_id(self):
        """ extension point with no Id """

        def factory():
            class Foo(TestBase):
                x = ExtensionPoint(List(Int))

        with self.assertRaises(ValueError):
            factory()

    def test_set_untyped_extension_point(self):
        """ set untyped extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Declare a class that consumes the extension.
        class Foo(TestBase):
            x = ExtensionPoint(id='my.ep')

        # Make sure that when we set the trait the extension registry gets
        # updated.
        f = Foo()
        f.x = [42]

        self.assertEqual([42], registry.get_extensions('my.ep'))

    def test_set_typed_extension_point(self):
        """ set typed extension point """

        registry = self.registry

        # Add an extension point.
        registry.add_extension_point(self._create_extension_point('my.ep'))

        # Declare a class that consumes the extension.
        class Foo(TestBase):
            x = ExtensionPoint(List(Int), id='my.ep')

        # Make sure that when we set the trait the extension registry gets
        # updated.
        f = Foo()
        f.x = [42]

        self.assertEqual([42], registry.get_extensions('my.ep'))

    def test_extension_point_str_representation(self):
        """ test the string representation of the extension point """
        ep_repr = "ExtensionPoint(id={})"
        ep = self._create_extension_point('my.ep')
        self.assertEqual(ep_repr.format('my.ep'), str(ep))
        self.assertEqual(ep_repr.format('my.ep'), repr(ep))

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_extension_point(self, id, trait_type=List, desc=''):
        """ Create an extension point. """

        return ExtensionPoint(id=id, trait_type=trait_type, desc=desc)
