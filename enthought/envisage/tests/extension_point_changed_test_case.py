""" Tests for the events fired when extension points are changed. """


# Standard library imports.
import unittest

# Enthought library imports.
##from enthought.envisage.api import ExtensionPoint

# Local imports.
from application_test_case import ExtensionPoint, PluginA, PluginB, PluginC
from application_test_case import TestApplication, listener

    
class ExtensionPointChangedTestCase(unittest.TestCase):
    """ Tests for the events fired when extension points are changed. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # Make sure that the listener contents get cleand up before each test.
        listener.obj = None
        listener.trait_name = None
        listener.old = None
        listener.new = None

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_set_extension_point(self):
        """ set extension point """

        a = PluginA()

        application = TestApplication(plugins=[a])
        application.start()

        # Try to set the extension point.
        self.failUnlessRaises(SystemError, setattr, a, 'x', [1, 2, 3])
        
        return

    def test_append(self):
        """ append """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()
        
        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)
        
        # Append a contribution.
        b.x.append(4)

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(7, len(extensions))
        self.assertEqual([1, 2, 3, 4, 98, 99, 100], extensions)

        # Make sure we pick up the new contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(7, len(extensions))
        self.assertEqual([1, 2, 3, 4, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([4], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)
        
        return

    def test_remove(self):
        """ remove """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()
        
        application = TestApplication(plugins=[a, b, c])
        application.start()
        
        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Remove a contribution.
        b.x.remove(3)

        # Make sure we pick up the correct contributions via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(5, len(extensions))
        self.assertEqual([1, 2, 98, 99, 100], extensions)

        # Make sure we pick up the correct contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(5, len(extensions))
        self.assertEqual([1, 2, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([3], listener.new.removed)
        self.assertEqual(2, listener.new.index)

        return

    def test_assign_empty_list(self):
        """ assign empty list """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()
        
        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)

        # Assign an empty list to one of the plugin's contributions
        b.x = []

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we pick up the correct contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index.start)
        self.assertEqual(3, listener.new.index.stop)
        
        return

    def test_assign_non_empty_list(self):
        """ assign non-empty list """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()
        
        application = TestApplication(plugins=[a, b, c])
        application.start()

        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3, 98, 99, 100], a.x)
        
        # Assign a non-empty list to one of the plugin's contributions.
        b.x = [2, 4, 6, 8]

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(7, len(extensions))
        self.assertEqual([2, 4, 6, 8, 98, 99, 100], extensions)

        # Make sure we pick up the new contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(7, len(extensions))
        self.assertEqual([2, 4, 6, 8, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([2, 4, 6, 8], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index.start)
        self.assertEqual(4, listener.new.index.stop)
        
        return

    def test_add_plugin(self):
        """ add plugin """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()
        
        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Now add the other plugin.
        application.plugins.append(c)

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()

        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([98, 99, 100], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)
        
        return

    def test_remove_plugin(self):
        """ remove plugin """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()
        c = PluginC()
        
        application = TestApplication(plugins=[a, b, c])
        application.start()
        
        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()

        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Now remove one plugin.
        application.plugins.remove(b)

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index)
        
        return

#### EOF ######################################################################
