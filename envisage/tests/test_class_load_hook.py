# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for class load hooks. """


from envisage.api import ClassLoadHook
from traits.api import HasTraits
from traits.testing.unittest_tools import unittest


# This module's package.
PKG = 'envisage.tests'


class ClassLoadHookTestCase(unittest.TestCase):
    """ Tests for class load hooks. """

    def test_connect(self):
        """ connect """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name = ClassLoadHookTestCase.__module__ + '.Foo',
            on_load    = on_class_loaded
        )
        hook.connect()

        class Foo(HasTraits):
            pass

        self.assertEqual(Foo, on_class_loaded.cls)

    def test_class_already_loaded(self):
        """ class already loaded """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name = self._get_full_class_name(ClassLoadHookTestCase),
            on_load    = on_class_loaded
        )
        hook.connect()

        # Make sure the 'on_load' got called immediately because the class is
        # already loaded.
        self.assertEqual(ClassLoadHookTestCase, on_class_loaded.cls)

    def test_disconnect(self):
        """ disconnect """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name = ClassLoadHookTestCase.__module__ + '.Foo',
            on_load    = on_class_loaded
        )
        hook.connect()

        class Foo(HasTraits):
            pass

        self.assertEqual(Foo, on_class_loaded.cls)

        # 'Reset' the listener,
        on_class_loaded.cls = None

        # Now disconnect.
        hook.disconnect()

        class Foo(HasTraits):
            pass

        self.assertEqual(None, on_class_loaded.cls)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_full_class_name(self, cls):
        """ Return the full (possibly) dotted name of a class. """

        return cls.__module__ + '.' + cls.__name__
