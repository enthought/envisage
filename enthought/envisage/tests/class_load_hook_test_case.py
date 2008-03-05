""" Tests for class load hooks. """


# Standard library imports.
import sys, unittest

# Enthought library imports.
from enthought.envisage.api import CategoryImporter, ClassLoadHook
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

    def test_category_importer(self):
        """ category importer """

        category = CategoryImporter(
            class_name          = 'bar.Bar',
            category_class_name = 'bar_category.BarCategory',
        )
        category.connect()
        
        # Import the target class.
        from bar import Bar

        # Make sure the category was added!
        self.assert_('y' in Bar.class_traits())

        # Try another one now that the class is already loaded.
        category = CategoryImporter(
            class_name          = 'bar.Bar',
            category_class_name = 'baz_category.BazCategory',
        )

        # The 'BazCategory' shouldn't be there yet!
        self.assert_('z' not in Bar.class_traits())

        # But when we 'connect' the class load hook, it should realise that
        # the class is already loaded and add the category to it straight
        # away.
        category.connect()

        # Make sure the category was added!
        self.assert_('z' in Bar.class_traits())
        
        return

# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()
    
#### EOF ######################################################################
