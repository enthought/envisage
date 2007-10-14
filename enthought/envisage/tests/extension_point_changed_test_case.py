""" Tests for the events fired when extension points are changed. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, Plugin
from enthought.envisage.api import PluginManager
from enthought.traits.api import HasTraits, Int, List


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


class TestApplication(Application):
    """ The type of application used in the tests.

    This applications uses a plugin manager that is manually populated (the
    default plugin manager uses Python Eggs).

    """

    def _plugin_manager_default(self):
        """ Trait initializer. """

        return PluginManager(application=self)


def ExtensionPoint(trait_type, id):
    """ A factory function for extension point traits. """
    
    import inspect

    if inspect.isclass(trait_type):
        trait_type = trait_type()

    # fixme: There must be a better API than this to add metadata to a trait?
    trait_type._metadata['__extension_point_id__'] = id
    
    return  trait_type


class PluginA(Plugin):
    id = 'A'
    x  = ExtensionPoint(List, id='a.x')


class PluginB(Plugin):
    id = 'B'
    x  = List(Int, [1, 2, 3], extension_point='a.x')


class PluginC(Plugin):
    id = 'C'
    x  = List(Int, [4, 5, 6], extension_point='a.x')

    
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

    # fixme: This doesn't work when tryoing the extension poin tbinding way
    # since we don't control the trait set... maybe we should set the trait
    # type's setter?
    def Xtest_set_extension_point(self):
        """ set extension point """

        a = PluginA()

        application = TestApplication(id='test', plugins=[a])
        application.start()

        # Try to set the extension point.
        self.failUnlessRaises(SystemError, setattr, a, 'x', [1, 2, 3])
        
        return

    def test_append(self):
        """ append """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()

        application = TestApplication(id='test', plugins=[a, b])
        application.start()

        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3], a.x)
        
        # Append a contribution.
        b.x.append(99)

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(4, len(extensions))
        self.assertEqual([1, 2, 3, 99], extensions)

        # Make sure we pick up the new contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(4, len(extensions))
        self.assertEqual([1, 2, 3, 99], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([99], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(3, listener.new.index)
        
        return

    def test_remove(self):
        """ remove """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()

        application = TestApplication(id='test', plugins=[a, b])
        application.start()
        
        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3], a.x)

        # Remove a contribution.
        b.x.remove(3)

        # Make sure we pick up the correct contributions via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(2, len(extensions))
        self.assertEqual([1, 2], extensions)

        # Make sure we pick up the correct contributions via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(2, len(extensions))
        self.assertEqual([1, 2], extensions)

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

        application = TestApplication(id='test', plugins=[a, b])
        application.start()

        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3], a.x)

        # Assign an empty list to the plugin's contributions
        b.x = []

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(0, len(extensions))

        # Make sure we pick up the correct contribution via the plugin.
        extensions = a.x[:]
        self.assertEqual(0, len(extensions))

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

        application = TestApplication(id='test', plugins=[a, b])
        application.start()

        # fixme: Currently we only wire up the listeners the first time we get
        # the extensions.
        self.assertEqual([1, 2, 3], a.x)
        
        # Assign a non-empty list to the plugin's contributions.
        b.x = [2, 4, 6, 8]

        # Make sure we pick up the new contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(4, len(extensions))
        self.assertEqual([2, 4, 6, 8], extensions)

        # Make sure we pick up the new contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(4, len(extensions))
        self.assertEqual([2, 4, 6, 8], extensions)

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

        # Start off with just one of the plugins.
        application = TestApplication(id='test', plugins=[a])
        application.start()
        
        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(0, len(extensions))

        # Make sure we pick up the correct contribution via the plugin.
        self.assertEqual(0, len(a.x))

        # Now add the other plugin.
        application.plugins.append(b)

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Make sure we pick up the correct contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([1, 2, 3], listener.new.added)
        self.assertEqual([], listener.new.removed)
        self.assertEqual(0, listener.new.index)
        
        return

    def test_remove_plugin(self):
        """ remove plugin """

        a = PluginA(); a.on_trait_change(listener, 'x_items')
        b = PluginB()

        # Start off with just one of the plugins.
        application = TestApplication(id='test', plugins=[a, b])
        application.start()

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
        extensions.sort()

        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Make sure we pick up the correct contribution via the plugin.
        extensions = a.x[:]
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Now remove the plugin that made the contributions.
        application.plugins.remove(b)

        # Make sure we pick up the correct contribution via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(0, len(extensions))

        # Make sure we pick up the correct contribution via the plugin.
        self.assertEqual(0, len(a.x))

        # Make sure we got a trait event telling us that the contributions
        # to the extension point have been changed.
        self.assertEqual(a, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([], listener.new.added)
        self.assertEqual([1, 2, 3], listener.new.removed)
        self.assertEqual(0, listener.new.index)
        
        return

#### EOF ######################################################################
