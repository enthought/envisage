""" Tests for applications. """


# Enthought library imports.
from enthought.envisage.api import Application, PluginManager

# Local imports.
from event_tracker import EventTracker
from plugin_manager_test_case import PluginManagerTestCase
from service_registry_test_case import ServiceRegistryTestCase


def vetoer(event):
    """ A function that will veto an event. """
    
    event.veto = True

    return


class ApplicationTestCase(ServiceRegistryTestCase, PluginManagerTestCase):
    """ Tests for applications. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.application = Application(id=__name__)
        
        self.event_tracker  = EventTracker(
            subscriptions = [
                (self.application, 'starting'),
                (self.application, 'started'),
                (self.application, 'stopping'),
                (self.application, 'stopped')
            ]
        )

        # The application offers the service registry interface so we do all of
        # the usual service registry tests.
        self.service_registry = self.application

        # The application offers the service registry interface so we do all of
        # the usual service registry tests.
        self.application.plugin_manager = self.plugin_manager = PluginManager()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_no_plugins(self):
        """ no plugins """
        
        application = self.application
        tracker = self.event_tracker

        # Start.
        started = application.start()
        self.assertEqual(['starting', 'started'], tracker.event_names)
        self.assertEqual(True, started)
        
        # Stop.
        stopped = application.stop()
        self.assertEqual(
            ['starting', 'started', 'stopping', 'stopped'], tracker.event_names
        )
        self.assertEqual(True, stopped)

        return

    def test_veto_starting(self):
        """ veto starting """

        application = self.application
        tracker = self.event_tracker

        application.on_trait_change(vetoer, 'starting')
        
        # Start.
        started = application.start()
        self.assertEqual(['starting'], tracker.event_names)
        self.assertEqual(False, started)

        return

    def test_veto_stopping(self):
        """ veto stopping """

        application = self.application
        tracker = self.event_tracker

        application.on_trait_change(vetoer, 'stopping')

        # Start.
        started = application.start()
        self.assertEqual(['starting', 'started'], tracker.event_names)
        self.assertEqual(True, started)
        
        # Stop.
        stopped = application.stop()
        self.assertEqual(
            ['starting', 'started', 'stopping'], tracker.event_names
        )
        self.assertEqual(False, stopped)

        return

#### EOF ######################################################################
