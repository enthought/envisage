""" Tests for trait list events. """


# Standard library imports.
import random, unittest

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, Plugin
from enthought.envisage.api import PluginManager, bind_extension_point
from enthought.traits.api import HasTraits, Instance, Int, Interface, List, Str
from enthought.traits.api import implements


def listener(obj, trait_name, old, event):
    """ Create the original list from a trait list event. """

    # Ignore the '_items' part of the trait name (if it is there!).
    trait_name = trait_name.split('_items')[0]

    original = getattr(obj, trait_name)[:]

    if isinstance(event.index, slice):
        original[event.index] = event.removed[0]

    else:
        original[event.index : event.index + len(event.added)] = event.removed
    
    listener.original = original

    return


class SliceTestCase(unittest.TestCase):
    """ Tests for trait list events. """

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

    def test_del(self):
        """ del """

        original = range(10)
        
        class Foo(HasTraits):
            l = List

        f = Foo(l=original)
        f.on_trait_change(listener, 'l_items')

        # Delete an item.
        del f.l[5:9]

        # Make sure we get the original.
        self.assertEqual(original, listener.original)

        return
    
    def test_slice(self):
        """ slice """

        original = range(10)
        
        class Foo(HasTraits):
            l = List

        f = Foo(l=original)
        f.on_trait_change(listener, 'l_items')

        # Replace a slice.
        f.l[2:6:2] = [88, 99]

        # Make sure we get the original.
        self.assertEqual(original, listener.original)

        return
    
#### EOF ######################################################################
