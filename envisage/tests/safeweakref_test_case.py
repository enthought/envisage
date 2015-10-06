""" Tests for safe weakrefs. """


# Standard library imports.
import weakref

# Enthought library imports.
from envisage.safeweakref import ref
from traits.api import HasTraits
from traits.testing.unittest_tools import unittest


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

    def test_can_create_weakref_to_bound_method(self):
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

    def test_two_weakrefs_to_bound_method_are_identical(self):
        class Foo(HasTraits):
            def method(self):
                pass

        f = Foo()

        self.assertIs(ref(f.method), ref(f.method))

        return

    def test_internal_cache_is_weak_too(self):
        # smell: Fragile test because we are reaching into the internals of the
        # object under test.
        #
        # I can't see a (clean!) way around this without adding something to
        # the public API that would only exist for testing, but in terms of
        # 'bang for the buck' I think this is good enough despite the
        # fragility.
        cache = ref._cache

        class Foo(HasTraits):
            def method(self):
                pass

        f = Foo()

        # Get the length of the cache before we do anything.
        len_cache = len(cache)

        # Create a weak reference to the bound method and make sure that
        # exactly one item has been added to the cache.
        r = ref(f.method)
        self.assertEqual(len_cache + 1, len(cache))

        # Delete the instance!
        del f

        # Our `ref` should now reference nothing...
        self.assertEqual(None, r())

        # ... and the cache should be back to its original size!
        self.assertEqual(len_cache, len(cache))

        return

    def test_two_weakrefs_to_bound_method_are_equal(self):
        class Foo(HasTraits):
            def method(self):
                pass

        f = Foo()

        # Make sure that two references to the same method compare as equal.
        r1 = ref(f.method)
        r2 = ref(f.method)
        self.assertEqual(r1, r2)

        # Make sure that a reference compares as unequal to non-references!
        self.assert_(not r1 == 99)

        return

    def test_two_weakrefs_to_bound_method_hash_equally(self):
        class Foo(HasTraits):
            def method(self):
                pass

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

    def test_get_builtin_weakref_for_non_bound_method(self):
        class Foo(HasTraits):
            pass

        f = Foo()

        # Get a weak reference to something that is not a bound method.
        r = ref(f)
        self.assertEqual(weakref.ref, type(r))

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
