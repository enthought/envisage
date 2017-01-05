""" Tests to help find out how trait list events work.

These tests exist because when we are using the 'ExtensionPoint' trait type
we try to mimic trait list events when extensions are added or removed.

"""


# Enthought library imports.
from traits.api import HasTraits, List
from traits.testing.unittest_tools import unittest


# The starting list for all tests.
TEST_LIST = [7, 9, 2, 3, 4, 1, 6, 5, 8, 0]


def listener(obj, trait_name, old, event):
    """ Recreate a list operation from a trait list event. """

    clone = TEST_LIST[:]

    # If nothing was added then this is a 'del' or 'remove' operation.
    if len(event.added) == 0:
        if isinstance(event.index, slice):
            del clone[event.index]

        else:
            # workaroud for traits bug in Python 3
            # https://github.com/enthought/traits/issues/334
            index = event.index if event.index is not None else 0
            del clone[index:index + len(event.removed)]

    # If nothing was removed then it is an 'append', 'insert' or 'extend'
    # operation.
    elif len(event.removed) == 0:
        if isinstance(event.index, slice):
            clone[event.index] = event.added[0]

        else:
            clone.insert(event.index, event.added[0])

    # Otherwise, it is an assigment ('sort' and 'reverse' fall into this
    # category).
    else:
        if isinstance(event.index, slice):
            clone[event.index] = event.added[0]

        else:
            clone[event.index : event.index + len(event.added)] = event.added

    listener.clone = clone

    return


class SliceTestCase(unittest.TestCase):
    """ Tests to help find out how trait list events work. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        class Foo(HasTraits):
            l = List

        self.f = Foo(l=TEST_LIST)
        self.f.on_trait_change(listener, 'l_items')

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.l, listener.clone)

        return

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_append(self):
        """ append """

        self.f.l.append(99)

        return

    def test_insert(self):
        """ insert """

        self.f.l.insert(3, 99)

        return

    def test_extend(self):
        """ extend """

        self.f.l.append([99, 100])

        return

    def test_remove(self):
        """ remove """

        self.f.l.remove(5)

        return

    def test_reverse(self):
        """ reverse """

        self.f.l.reverse()

        return

    def test_sort(self):
        """ sort """

        self.f.l.sort()

        return

    def test_pop(self):
        """ remove """

        self.f.l.pop()

        return

    def test_del_all(self):
        """ del all """

        del self.f.l[:]

        return

    def test_assign_item(self):
        """ assign item """

        self.f.l[3] = 99

        return

    def test_del_item(self):
        """ del item """

        del self.f.l[3]

        return

    def test_assign_slice(self):
        """ assign slice """

        self.f.l[2:4] = [88, 99]

        return

    def test_del_slice(self):
        """ del slice """

        del self.f.l[2:5]

        return

    def test_assign_extended_slice(self):
        """ assign extended slice """

        self.f.l[2:6:2] = [88, 99]

        return

    def test_del_extended_slice(self):
        """ del extended slice """

        del self.f.l[2:6:2]

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
