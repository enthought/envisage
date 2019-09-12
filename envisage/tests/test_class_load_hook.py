""" Tests for class load hooks. """


from envisage.api import ClassLoadHook
from traits.api import HasTraits
from traits.testing.unittest_tools import unittest


# This module's package.
PKG = 'envisage.tests'


class ClassLoadHookTestCase(unittest.TestCase):
    """ Tests for class load hooks. """

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

    def test_connect(self):
        """ connect """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

            return

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name = ClassLoadHookTestCase.__module__ + '.Foo',
            on_load    = on_class_loaded
        )
        hook.connect()

        class Foo(HasTraits):
            pass

        self.assertEqual(Foo, on_class_loaded.cls)

        return

    def test_class_already_loaded(self):
        """ class already loaded """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

            return

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name = self._get_full_class_name(ClassLoadHookTestCase),
            on_load    = on_class_loaded
        )
        hook.connect()

        # Make sure the 'on_load' got called immediately because the class is
        # already loaded.
        self.assertEqual(ClassLoadHookTestCase, on_class_loaded.cls)

        return

    def test_disconnect(self):
        """ disconnect """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

            return

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

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_full_class_name(self, cls):
        """ Return the full (possibly) dotted name of a class. """

        return cls.__module__ + '.' + cls.__name__


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
