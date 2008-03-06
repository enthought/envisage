""" Tests for class load hooks. """


# Standard library imports.
import sys, unittest

# Enthought library imports.
from enthought.traits.api import HasTraits

# fixme: Should these be in the api?
from enthought.envisage.class_load_hook import ClassLoadHook


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
            class_name='class_load_hook_test_case.Foo', on_load=on_class_loaded
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

        # Create the class before we create the hook.
        class Bar(HasTraits):
            pass

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name = 'class_load_hook_test_case.ClassLoadHookTestCase',
            on_load    = on_class_loaded
        )
        hook.connect()
        
        return

    def test_disconnect(self):
        """ disconnect """

        def on_class_loaded(cls):
            """ Called when a class is loaded. """

            on_class_loaded.cls = cls

            return

        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ClassLoadHook(
            class_name='class_load_hook_test_case.Foo', on_load=on_class_loaded
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


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()
    
#### EOF ######################################################################
