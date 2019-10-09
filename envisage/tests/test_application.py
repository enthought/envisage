# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for applications and plugins. """


# Standard library imports.
import os
import shutil
import tempfile
import unittest

# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from envisage.api import Application, ExtensionPoint
from envisage.api import Plugin, PluginManager
from traits.api import Bool, Int, List

# Local imports.
from envisage.tests.event_tracker import EventTracker
from envisage.tests.ets_config_patcher import ETSConfigPatcher


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new


def vetoer(event):
    """ A function that will veto an event. """

    event.veto = True


class TestApplication(Application):
    """ The type of application used in the tests. """

    id = 'test'


class SimplePlugin(Plugin):
    """ A simple plugin. """

    #### 'SimplePlugin' interface #############################################

    started = Bool(False)
    stopped = Bool(False)

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        self.started = True
        self.stopped = False

    def stop(self):
        """ Stop the plugin. """

        self.started = False
        self.stopped = True


class BadPlugin(Plugin):
    """ A plugin that just causes trouble ;^). """

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        raise 1/0

    def stop(self):
        """ Stop the plugin. """

        raise 1/0


class PluginA(Plugin):
    """ A plugin that offers an extension point. """

    id = 'A'
    x  = ExtensionPoint(List, id='a.x')


class PluginB(Plugin):
    """ A plugin that contributes to an extension point. """

    id = 'B'
    x  = List(Int, [1, 2, 3], contributes_to='a.x')


class PluginC(Plugin):
    """ Another plugin that contributes to an extension point! """

    id = 'C'
    x  = List(Int, [98, 99, 100], contributes_to='a.x')


class ApplicationTestCase(unittest.TestCase):
    """ Tests for applications and plugins. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # Make sure that the listener contents get cleand up before each test.
        listener.obj = None
        listener.trait_name = None
        listener.old = None
        listener.new = None

        ets_config_patcher = ETSConfigPatcher()
        ets_config_patcher.start()
        self.addCleanup(ets_config_patcher.stop)

    def test_home(self):
        """ home """

        application = TestApplication()

        # Make sure we get the right default value.
        self.assertEqual(ETSConfig.application_home, application.home)

        # Delete the directory.
        shutil.rmtree(application.home)

        # Create a new application.
        application = TestApplication()

        # Make sure the directory got created.
        self.assertTrue(os.path.exists(application.home))

        # Delete the directory.
        shutil.rmtree(application.home)

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
        self.assertTrue('started' not in tracker.event_names)

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
        self.assertTrue('stopped' not in tracker.event_names)

    def test_start_and_stop_errors(self):
        """ start and stop errors """

        simple_plugin = SimplePlugin()
        bad_plugin    = BadPlugin()
        application   = TestApplication(plugins=[simple_plugin, bad_plugin])

        # Try to start the application - the bad plugin should barf.
        with self.assertRaises(ZeroDivisionError):
            application.start()

        # Try to stop the application - the bad plugin should barf.
        with self.assertRaises(ZeroDivisionError):
            application.stop()

        # Try to start a non-existent plugin.
        with self.assertRaises(SystemError):
            application.start_plugin(plugin_id="bogus")

        # Try to stop a non-existent plugin.
        with self.assertRaises(SystemError):
            application.stop_plugin(plugin_id="bogus")

    def test_extension_point(self):
        """ extension point """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

    def test_add_extension_point_listener(self):
        """ add extension point listener """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b])
        application.start()

        def listener(extension_registry, event):
            """ An extension point listener. """

            listener.extension_point_id = event.extension_point_id
            listener.added              = event.added
            listener.removed            = event.removed

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Add the listener.
        application.add_extension_point_listener(listener, 'a.x')

        # Now add the other plugin.
        application.add_plugin(c)

        # Make sure the listener was called.
        self.assertEqual('a.x', listener.extension_point_id)
        self.assertEqual([], listener.removed)
        self.assertEqual([98, 99, 100], listener.added)

    def test_remove_extension_point_listener(self):
        """ remove extension point listener """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        # Start off with just one of the plugins.
        application = TestApplication(plugins=[a])
        application.start()

        def listener(extension_registry, event):
            """ An extension point listener. """

            listener.extension_point_id = event.extension_point_id
            listener.added   = event.added
            listener.removed = event.removed

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(0, len(extensions))

        # Add the listener.
        application.add_extension_point_listener(listener, 'a.x')

        # Now add one of the other plugins.
        application.add_plugin(b)

        # Make sure the listener was called.
        self.assertEqual('a.x', listener.extension_point_id)
        self.assertEqual([], listener.removed)
        self.assertEqual([1, 2, 3], listener.added)

        # Now remove the listener.
        listener.extension_point_id = None
        application.remove_extension_point_listener(listener, 'a.x')

        # Now add the final plugin.
        application.add_plugin(c)

        # Make sure the listener was *not* called.
        self.assertEqual(None, listener.extension_point_id)

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
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x
        self.assertEqual(3, len(extensions))
        self.assertEqual([1, 2, 3], extensions)

        # Now add the other plugin.
        application.add_plugin(c)

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

    def test_get_plugin(self):
        """ get plugin """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        # Start off with just two of the plugins.
        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Make sure we can get the plugins.
        self.assertEqual(a, application.get_plugin('A'))
        self.assertEqual(b, application.get_plugin('B'))
        self.assertEqual(c, application.get_plugin('C'))

        # Make sure we can't get one that isn't there ;^)
        self.assertEqual(None, application.get_plugin('BOGUS'))

    def test_remove_plugin(self):
        """ remove plugin """

        a = PluginA()
        b = PluginB()
        c = PluginC()

        application = TestApplication(plugins=[a, b, c])
        application.start()

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x
        self.assertEqual(6, len(extensions))
        self.assertEqual([1, 2, 3, 98, 99, 100], extensions)

        # Now remove one plugin.
        application.remove_plugin(b)

        # Make sure we can get the contributions via the application.
        extensions = application.get_extensions('a.x')
        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

        # Make sure we can get the contributions via the plugin.
        extensions = a.x
        self.assertEqual(3, len(extensions))
        self.assertEqual([98, 99, 100], extensions)

    def test_set_plugin_manager_at_contruction_time(self):
        """ set plugin manager at construction time"""

        a = PluginA()
        b = PluginB()
        c = PluginC()

        # Start off with just two of the plugins.
        application = TestApplication(
            plugin_manager=PluginManager(plugins=[a, b, c])
        )
        application.start()

        # Make sure we can get the plugins.
        self.assertEqual(a, application.get_plugin('A'))
        self.assertEqual(b, application.get_plugin('B'))
        self.assertEqual(c, application.get_plugin('C'))

        # Make sure we can't get one that isn't there ;^)
        self.assertEqual(None, application.get_plugin('BOGUS'))
