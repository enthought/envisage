""" Tests for plugins. """


# Standard library imports.
import random, unittest

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, Plugin
from enthought.envisage.api import PluginManager, connect_extension_point
from enthought.traits.api import HasTraits, Instance, Int, Interface, List, Str
from enthought.traits.api import implements


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


class TestApplication(Application):
    """ The type of application used in the tests. """

    def _plugin_manager_default(self):
        """ Trait initializer. """

        return PluginManager(application=self)

    
class PluginTestCase(unittest.TestCase):
    """ Tests for plugins. """

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

    def test_add_plugin(self):
        """ add plugin """

        class PluginA(Plugin):
            id = 'A'
            x  = List(Int, [1, 2, 3], extension_point='x')

        class PluginB(Plugin):
            id = 'B'
            x  = List(Int, [4, 5, 6], extension_point='x')

        a = PluginA()
        b = PluginB()

        # Start off with just one of the plugins.
        application = TestApplication(id='plugin.test.case', plugins=[a])
        application.start()
        
        # Make sure we get the plugin's contributions.
        extensions = application.get_extensions('x')
        extensions.sort()
        
        self.assertEqual([1, 2, 3], extensions)

        # Now add the other plugin.
##        application.plugins.append(b)
        application.add_plugin(b)

        # Make sure we get the other plugin's contributions too.
        extensions = application.get_extensions('x')
        extensions.sort()
        
        self.assertEqual(6, len(application.get_extensions('x')))
        self.assertEqual([1, 2, 3, 4, 5, 6], extensions)

        return

    def test_service(self):
        """ service """

        class Foo(HasTraits):
            pass

        class PluginA(Plugin):
            id = 'A'
            foo = Instance(Foo, (), service=True)

        a = PluginA()

        application = TestApplication(id='plugin.test.case', plugins=[a])
        application.start()

        # Make sure the service was registered.
        self.assertNotEqual(None, application.get_service(Foo))
        self.assertEqual(a.foo, application.get_service(Foo))

        application.stop()

        # Make sure the service was unregistered.
        self.assertEqual(None, application.get_service(Foo))

        return

    def test_service_protocol(self):
        """ service protocol """

        class IFoo(Interface):
            pass

        class IBar(Interface):
            pass
        
        class Foo(HasTraits):
            implements(IFoo, IBar)

        class PluginA(Plugin):
            id = 'A'
            foo = Instance(Foo, (), service=True, service_protocol=IBar)
            
        a = PluginA()
        
        application = TestApplication(id='plugin.test.case', plugins=[a])
        application.start()

        # Make sure the service was registered with the 'IBar' protocol.
        self.assertNotEqual(None, application.get_service(IBar))
        self.assertEqual(a.foo, application.get_service(IBar))

        application.stop()

        # Make sure the service was unregistered.
        self.assertEqual(None, application.get_service(IBar))

        return

    def test_extension_point_declarations(self):
        """ extension point declarations """

        class PluginA(Plugin):
            id = 'A'
            x  = ExtensionPoint(List, id='a.x')

        class PluginB(Plugin):
            id = 'B'
            x  = List(Int, [1, 2, 3], extension_point='a.x')

        a = PluginA()
        b = PluginB()

        application = TestApplication(id='plugin.test.case',plugins=[a, b])
        application.run()
        
        # Make sure we get all of the plugin's contributions.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)
        
        # Add another contribution to one of the plugins.
        b.x.append(99)

        # Make sure we have picked up the new contribution.
        extensions = application.get_extensions('a.x')
        extensions.sort()
        
        self.assertEqual(4, len(extensions))
        self.assertEqual([1, 2, 3, 99], extensions)

        return

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

        application = TestApplication(id='plugin.test.case', plugins=[a, b])

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

    def test_multiple_trait_contributions(self):
        """ multiple trait contributions """

        class PluginA(Plugin):
            id = 'A'
            x  = List(Int, [1, 2, 3], extension_point='x')
            y  = List(Int, [4, 5, 6], extension_point='x')

        a = PluginA()

        application = TestApplication(id='plugin.test.case', plugins=[a])

        # We should get an error because the plugin has multiple traits
        # contributing to the same extension point.
        self.failUnlessRaises(ValueError, application.get_extensions, 'x')

        return

    def test_trait_contributions_with_connection(self):
        """ trait contributions with connection """

        class PluginA(Plugin):
            id = 'A'
            x  = List(Int, [1, 2, 3], extension_point='x')

        class PluginB(Plugin):
            id = 'B'
            x  = List(Int, [4, 5, 6], extension_point='x')

        a = PluginA()
        b = PluginB()

        application = TestApplication(id='plugin.test.case', plugins=[a, b])
        application.start()
        
        # Create an arbitrary object that has a trait bound to the extension
        # point.
        class Foo(HasTraits):
            """ A class! """

            x = List(Int)

        f = Foo(); connect_extension_point(f, 'x', 'x')
        f.on_trait_change(listener)

        # Make sure we get all of the plugin's contributions via the bound
        # trait.
        self.assertEqual([1, 2, 3, 4, 5, 6], f.x)
        
        # Add another contribution to one of the plugins.
        b.x.append(99)

        # Make sure that the correct trait change event was fired.
        self.assertEqual(f, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assert_(99 in listener.new.added)
        
        # Make sure we have picked up the new contribution via the bound trait.
        self.assertEqual([1, 2, 3, 4, 5, 6, 99], f.x)

        # Completley overwrite one of the plugins contributions
        b.x = [100, 101]

        # Make sure that the correct trait change event was fired.
        self.assertEqual(f, listener.obj)
        self.assertEqual('x_items', listener.trait_name)
        self.assertEqual([100, 101], listener.new.added)
        self.assertEqual([4, 5, 6, 99], listener.new.removed)
        
        # Make sure we have picked up the new contribution via the bound trait.
        self.assertEqual([1, 2, 3, 100, 101], f.x)

        return

    def test_preferences(self):
        """ preferences """

        class PluginA(Plugin):
            id = 'A'
            x  = List(
                ['file://preferences.ini'],
                extension_point='enthought.envisage.preferences'
            )

        a = PluginA()
        
        application = TestApplication(id='plugin.test.case', plugins=[a])
        application.run()

        # Make sure we can get one of the preferences.
        self.assertEqual('42', application.preferences.get('enthought.test.x'))

        return
    
#### EOF ######################################################################
