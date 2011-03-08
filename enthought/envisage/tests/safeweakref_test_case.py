""" Tests for safe weakrefs. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.safeweakref import ref
from enthought.traits.api import HasTraits

    
class SafeWeakrefTestCase(unittest.TestCase):
    """ Tests for safe weakrefs. """

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

    def test_bound_method(self):
        """ bound method """

        class Foo(HasTraits):
            def method(self):
                self.method_called = True

        f = Foo()

        # Get a weak reference to a bound method.
        r = ref(f.method)
        self.assertNotEqual(None, r())

        # Make sure we can call it.
        r()()
        self.assert_(f.method_called)

        # Delete the object to delete the method!
        del f

        # The reference should now return None.
        self.assertEqual(None, r())
        
        return

    def test_is(self):
        """ is """

        class Foo(HasTraits):
            def method(self):
                self.method_called = True

        f = Foo()

        # Make sure that two references to the same method are identical.
        self.assert_(ref(f.method) is ref(f.method))
        
        return

    def test_cache_is_weak_too(self):
        """ cache is weak too """

        class Foo(HasTraits):
            def method(self):
                self.method_called = True

        f = Foo()
        r = ref(f.method)
        
        # Delete the instance!
        del f

        # Our `ref` should now reference nothing...
        self.assertEqual(None, r())

        # ... and the cache should be empty!
        #
        # fixme: Reaching into internals to test!
        self.assertEqual(0, len(ref._cache))
        
        return

    def test_cmp(self):
        """ cmp """

        class Foo(HasTraits):
            def method(self):
                self.method_called = True

        f = Foo()

        # Make sure that two references to the same method compare as equal.
        r1 = ref(f.method)
        r2 = ref(f.method)
        self.assertEqual(r1, r2)

        # Make sure that a reference compares as unequal to non-references!
        self.assert_(not r1 == 99)
        
        return

    def test_hash(self):
        """ hash """

        class Foo(HasTraits):
            def method(self):
                self.method_called = True

        f = Foo()

        # Make sure we can hash the references.
        r1 = ref(f.method)
        r2 = ref(f.method)

        self.assertEqual(hash(r1), hash(r2))

        # Make sure we can hash non-bound methods.
        r1 = ref(Foo)
        r2 = ref(Foo)

        self.assertEqual(hash(r1), hash(r2))
        
        return

    def test_non_bound_method(self):
        """ non bound method """

        class Foo(HasTraits):
            pass

        f = Foo()

        # Get a weak reference to something that is not a bound method.
        r = ref(f)
        self.assertNotEqual(None, r())

        # Delete the object.
        del f

        # The reference should now return None.
        self.assertEqual(None, r())
        
        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
