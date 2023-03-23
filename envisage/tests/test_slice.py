# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests to help find out how trait list events work.

These tests exist because when we are using the 'ExtensionPoint' trait type
we try to mimic trait list events when extensions are added or removed.

"""

# Standard library imports.
import unittest

# Enthought library imports.
from traits.api import HasTraits, List

# The starting list for all tests.
TEST_LIST = [7, 9, 2, 3, 4, 1, 6, 5, 8, 0]


def listener(obj, trait_name, old, event):
    """Recreate a list operation from a trait list event."""

    clone = TEST_LIST[:]

    added = event.added
    # Backwards compatibility for Traits < 6.0, where event.added may
    # be a list containing a list containing the added elements. This
    # block can be removed once compatibility with Traits < 6.0 is no
    # longer needed. Ref: enthought/traits#300.
    if len(added) == 1 and isinstance(added[0], list):
        added = added[0]

    # If nothing was added then this is a 'del' or 'remove' operation.
    if len(added) == 0:
        if isinstance(event.index, slice):
            del clone[event.index]

        else:
            # workaroud for traits bug in Python 3
            # https://github.com/enthought/traits/issues/334
            index = event.index if event.index is not None else 0
            del clone[index : index + len(event.removed)]

    # If nothing was removed then it is an 'append', 'insert' or 'extend'
    # operation.
    elif len(event.removed) == 0:
        if isinstance(event.index, slice):
            clone[event.index] = added

        else:
            clone[event.index : event.index] = added

    # Otherwise, it is an assigment ('sort' and 'reverse' fall into this
    # category).
    else:
        if isinstance(event.index, slice):
            clone[event.index] = added

        else:
            clone[event.index : event.index + len(added)] = added

    listener.clone = clone


class SliceTestCase(unittest.TestCase):
    """Tests to help find out how trait list events work."""

    def setUp(self):
        """Prepares the test fixture before each test method is called."""

        class Foo(HasTraits):
            elts = List

        self.f = Foo(elts=TEST_LIST)
        self.f.on_trait_change(listener, "elts_items")

    def test_append(self):
        """append"""

        self.f.elts.append(99)
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_insert(self):
        """insert"""

        self.f.elts.insert(3, 99)
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_extend(self):
        """extend"""

        self.f.elts.extend([99, 100])
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_remove(self):
        """remove"""

        self.f.elts.remove(5)
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_reverse(self):
        """reverse"""

        self.f.elts.reverse()
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_sort(self):
        """sort"""

        self.f.elts.sort()
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_pop(self):
        """remove"""

        self.f.elts.pop()
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_del_all(self):
        """del all"""

        del self.f.elts[:]
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_assign_item(self):
        """assign item"""

        self.f.elts[3] = 99
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_del_item(self):
        """del item"""

        del self.f.elts[3]
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_assign_slice(self):
        """assign slice"""

        self.f.elts[2:4] = [88, 99]
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_del_slice(self):
        """del slice"""

        del self.f.elts[2:5]
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_assign_extended_slice(self):
        """assign extended slice"""

        self.f.elts[2:6:2] = [88, 99]
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)

    def test_del_extended_slice(self):
        """del extended slice"""

        del self.f.elts[2:6:2]
        # Make sure we successfully recreated the operation.
        self.assertEqual(self.f.elts, listener.clone)
