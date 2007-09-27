""" Tests for applications. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Application, Plugin, PluginManager
from enthought.envisage.api import bind_extension_point
from enthought.traits.api import HasTraits, Int, List


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


class NewTestCase(unittest.TestCase):
    """ Tests for applications. """

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

    def test_trait_contributions(self):
        """ trait contributions """

        class PluginA(Plugin):
            id = 'A'
            x  = List(Int, [1, 2, 3], extension_point='x')

        class PluginB(Plugin):
            id = 'B'
            x  = List(Int, [4, 5, 6], extension_point='x')

        a = PluginA()
        b = PluginB()

        application = Application(plugins=[a, b])

        # Make sure we get all of the plugin's contributions.
        extensions = application.get_extensions('x')
        extensions.sort()
        
        self.assertEqual(6, len(application.get_extensions('x')))
        self.assertEqual([1, 2, 3, 4, 5, 6], extensions)
        
        # Add another contribution to one of the plugins.
        a.x.append(99)

        # Make sure we have picked up the new contribution.
        extensions = application.get_extensions('x')
        extensions.sort()
        
        self.assertEqual(7, len(application.get_extensions('x')))
        self.assertEqual([1, 2, 3, 4, 5, 6, 99], extensions)

        return

    def test_trait_contributions_with_binding(self):
        """ trait contributions with binding """

        class PluginA(Plugin):
            id = 'A'
            x  = List(Int, [1, 2, 3], extension_point='x')

        class PluginB(Plugin):
            id = 'B'
            x  = List(Int, [4, 5, 6], extension_point='x')

        a = PluginA()
        b = PluginB()

        application = Application(plugins=[a, b])

        # Create an arbitrary object that has a trait bound to the extension
        # point.
        class Foo(HasTraits):
            """ A class! """

            x = List(Int)

        f = Foo(); bind_extension_point(f, 'x', 'x')
        f.on_trait_change(listener)

        # Make sure we get all of the plugin's contributions via the bound
        # trait.
        f.x.sort()
        self.assertEqual(6, len(f.x))
        self.assertEqual([1, 2, 3, 4, 5, 6], f.x)
        
        # Add another contribution to one of the plugins.
        b.x.append(99)

        # Make sure that the correct trait change event was fired.
        self.assertEqual(f, listener.obj)
        self.assertEqual('x', listener.trait_name)
        self.assertEqual(7, len(listener.new))
        
        # Make sure we have picked up the new contribution via the bound trait.
        f.x.sort()
        self.assertEqual(7, len(f.x))
        self.assertEqual([1, 2, 3, 4, 5, 6, 99], f.x)

        return

#### EOF ######################################################################
