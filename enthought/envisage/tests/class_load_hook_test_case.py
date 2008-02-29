""" Tests for class load hooks. """


# Standard library imports.
import sys, unittest

# Enthought library imports.
from enthought.envisage.api import ClassLoadHook, ModuleImporter
from enthought.traits.api import HasTraits

    
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

    def test_module_importer(self):
        """ module importer """

        # The name of a built-in module to load when a class is loaded.
        # Obviously this is slightly dodgy because we can't be sure that some
        # other test hasn't imported the module already, but I've tried to
        # pick an obscure one ;^) I didn't want to import a local module 'cos
        # I know some test runners don't set the current working directory when
        # running harvested test suites. Seems lame to me, but hey...
        built_in = 'sndhdr'
        
        # To register with 'MetaHasTraits' we use 'module_name.class_name'.
        hook = ModuleImporter(
            class_name='class_load_hook_test_case.Foo', module_name=built_in
        )
        hook.connect()

        self.assert_(built_in not in sys.modules)

        class Foo(HasTraits):
            pass

        self.assert_(built_in in sys.modules)
        
        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()
    
#### EOF ######################################################################
