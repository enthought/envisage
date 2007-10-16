""" Tests for applications and plugins. """


# Standard library imports.
import random, unittest

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, IApplication
from enthought.envisage.api import Plugin, PluginManager
from enthought.envisage.api import connect_extension_point
from enthought.traits.api import HasTraits, Instance, Int, Interface, List, Str
from enthought.traits.api import implements

# Local imports.
from event_tracker import EventTracker


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


def vetoer(event):
    """ A function that will veto an event. """
    
    event.veto = True

    return


class _TestApplication(Application):
    """ The type of application used in the tests.

    This applications uses a plugin manager that is manually populated (the
    default plugin manager uses Python Eggs).

    """

    # The application's unique identifier.
    id = 'test'
    
    def _plugin_manager_default(self):
        """ Trait initializer. """

        return PluginManager(application=self)


def TestApplication(**traits):
    """ Factory function for creating type-safe applications! """
    
    application = _TestApplication(**traits)

    return IApplication(application)


class PluginA(Plugin):
    id = 'A'
    x  = ExtensionPoint(List, id='a.x')


class PluginB(Plugin):
    id = 'B'
    x  = List(Int, [1, 2, 3], extension_point='a.x')


class PluginC(Plugin):
    id = 'C'
    x  = List(Int, [98, 99, 100], extension_point='a.x')

    
class ApplicationTestCase(unittest.TestCase):
    """ Tests for applications and plugins. """

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

    def test_no_plugins(self):
        """ no plugins """

        application = TestApplication()
        
        tracker = EventTracker(
            subscriptions = [
                (application, 'starting'),
                (application, 'started'),
                (application, 'stopping'),
                (application, 'stopped')
            ]
        )

        # Start the application.
        started = application.start()
        self.assertEqual(True, started)
        self.assertEqual(['starting', 'started'], tracker.event_names)
        
        # Stop the application.
        stopped = application.stop()
        self.assertEqual(True, stopped)
        self.assertEqual(
            ['starting', 'started', 'stopping', 'stopped'], tracker.event_names
        )

        return

    def test_veto_starting(self):
        """ veto starting """

        application = TestApplication()

        # This listener will veto the 'starting' event.
        application.on_trait_change(vetoer, 'starting')

        tracker = EventTracker(
            subscriptions = [
                (application, 'starting'),
                (application, 'started'),
                (application, 'stopping'),
                (application, 'stopped')
            ]
        )

        # Start the application.
        started = application.start()
        self.assertEqual(False, started)
        self.assert_('started' not in tracker.event_names)

        return

    def test_veto_stopping(self):
        """ veto stopping """

        application = TestApplication()
        
        # This listener will veto the 'stopping' event.
        application.on_trait_change(vetoer, 'stopping')

        tracker = EventTracker(
            subscriptions = [
                (application, 'starting'),
                (application, 'started'),
                (application, 'stopping'),
                (application, 'stopped')
            ]
        )

        # Start the application.
        started = application.start()
        self.assertEqual(['starting', 'started'], tracker.event_names)
        self.assertEqual(True, started)
        
        # Stop the application.
        stopped = application.stop()
        self.assertEqual(False, stopped)
        self.assert_('stopped' not in tracker.event_names)

        return

    def test_extension_point(self):
        """ extension point """
        
        a = PluginA()
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
        
        return

    def test_add_plugin(self):
        """ add plugin """

        a = PluginA()
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
##         application.plugins.append(c)
        application.add_plugin(c)

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
        
        return

    def test_remove_plugin(self):
        """ remove plugin """

        a = PluginA()
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
##         application.plugins.remove(b)
        application.remove_plugin(b)

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
        
        return

    def test_preferences(self):
        """ preferences """

        class PluginA(Plugin):
            id = 'A'
            preferences = List(
                ['file://preferences.ini'],
                extension_point='enthought.envisage.preferences'
            )

        a = PluginA()
        
        application = TestApplication(plugins=[a])
        application.run()

        # Make sure we can get one of the preferences.
        self.assertEqual('42', application.preferences.get('enthought.test.x'))

        return
    
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
    
##     def test_service(self):
##         """ service """

##         class Foo(HasTraits):
##             pass

##         class PluginA(Plugin):
##             id = 'A'
##             foo = Instance(Foo, (), service=True)

##         a = PluginA()

##         application = TestApplication(plugins=[a])
##         application.start()

##         # Make sure the service was registered.
##         self.assertNotEqual(None, application.get_service(Foo))
##         self.assertEqual(a.foo, application.get_service(Foo))

##         application.stop()

##         # Make sure the service was unregistered.
##         self.assertEqual(None, application.get_service(Foo))

##         return

##     def test_service_protocol(self):
##         """ service protocol """

##         class IFoo(Interface):
##             pass

##         class IBar(Interface):
##             pass
        
##         class Foo(HasTraits):
##             implements(IFoo, IBar)

##         class PluginA(Plugin):
##             id = 'A'
##             foo = Instance(Foo, (), service=True, service_protocol=IBar)

##         a = PluginA()
        
##         application = TestApplication(plugins=[a])
##         application.start()

##         # Make sure the service was registered with the 'IBar' protocol.
##         self.assertNotEqual(None, application.get_service(IBar))
##         self.assertEqual(a.foo, application.get_service(IBar))

##         application.stop()

##         # Make sure the service was unregistered.
##         self.assertEqual(None, application.get_service(IBar))

##         return

##     def test_multiple_trait_contributions(self):
##         """ multiple trait contributions """

##         class PluginA(Plugin):
##             id = 'A'
##             x  = List(Int, [1, 2, 3], extension_point='x')
##             y  = List(Int, [4, 5, 6], extension_point='x')

##         a = PluginA()

##         application = TestApplication(plugins=[a])

##         # We should get an error because the plugin has multiple traits
##         # contributing to the same extension point.
##         self.failUnlessRaises(ValueError, application.get_extensions, 'x')

##         return

##     def test_trait_contributions_with_binding(self):
##         """ trait contributions with binding """

##         class PluginA(Plugin):
##             id = 'A'
##             x  = List(Int, [1, 2, 3], extension_point='x')

##         class PluginB(Plugin):
##             id = 'B'
##             x  = List(Int, [4, 5, 6], extension_point='x')

##         a = PluginA()
##         b = PluginB()

##         application = TestApplication(plugins=[a, b])

##         # Create an arbitrary object that has a trait bound to the extension
##         # point.
##         class Foo(HasTraits):
##             """ A class! """

##             x = List(Int)

##         f = Foo(); bind_extension_point(f, 'x', 'x')
##         f.on_trait_change(listener)

##         # Make sure we get all of the plugin's contributions via the bound
##         # trait.
##         self.assertEqual([1, 2, 3, 4, 5, 6], f.x)
        
##         # Add another contribution to one of the plugins.
##         b.x.append(99)

##         # Make sure that the correct trait change event was fired.
##         self.assertEqual(f, listener.obj)
##         self.assertEqual('x_items', listener.trait_name)
##         self.assert_(99 in listener.new.added)
        
##         # Make sure we have picked up the new contribution via the bound trait.
##         self.assertEqual([1, 2, 3, 4, 5, 6, 99], f.x)

##         # Completley overwrite one of the plugins contributions
##         b.x = [100, 101]

##         # Make sure that the correct trait change event was fired.
##         self.assertEqual(f, listener.obj)
##         self.assertEqual('x_items', listener.trait_name)
##         self.assertEqual([100, 101], listener.new.added)
##         self.assertEqual([4, 5, 6, 99], listener.new.removed)
        
##         # Make sure we have picked up the new contribution via the bound trait.
##         self.assertEqual([1, 2, 3, 100, 101], f.x)

##         return

#### EOF ######################################################################
