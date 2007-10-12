""" The application interface. """


# Enthought library imports.
from enthought.preferences.api import IPreferences
from enthought.traits.api import Event, Instance, Interface, List, Str
from enthought.traits.api import VetoableEvent

# Local imports.
from application_event import ApplicationEvent
from i_plugin import IPlugin


class IApplication(Interface):
    """ The application interface. """

    # A directory that the application can read and write to at will.
    home = Str

    # The application's globally unique identifier.
    id = Str

    # The root preferences node.
    preferences = Instance(IPreferences)
    
    # Fired when the application is starting. This is the first thing that
    # happens when the 'start' method is called.
    starting = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been started.
    started = Event(ApplicationEvent)

    # Fired when the plugin manager is stopping. This is the first thing that
    # happens when the 'stop' method is called.
    stopping = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been stopped.
    stopped = Event(ApplicationEvent)

    def add_extension_point_listener(self, listener, extension_point_id=None):
        """ Add a listener for extensions being added/removed.

        A listener is any Python callable with the following signature::

          def listener(extension_registry, extension_point_changed_event):

                ...

        If an extension point is specified then the listener will only be
        called when extensions are added to or removed from that extension
        point (the extension point may or may not have been added to the
        registry at the time of this call).
        
        If *no* extension point is specified then the listener will be called
        when extensions are added to or removed from *any* extension point.

        When extensions are added or removed all specific listeners are called
        first (in arbitrary order), followed by all non-specific listeners
        (again, in arbitrary order).
        
        """

    def add_extension_point(self, extension_point):
        """ Add an extension point.

        If an extension point already exists with this Id then it is simply
        replaced.

        """

    def get_extensions(self, extension_point_id):
        """ Return a list containing all contributions to an extension point.

        Return an empty list if the extension point does not exist.

        """

    def get_extension_point(self, extension_point_id):
        """ Return the extension point with the specified Id.

        Return None if no such extension point exists.

        """

    def get_extension_points(self):
        """ Return all extension points.

        """

    def get_plugin(self, plugin_id):
        """ Return the plugin with the specified Id.

        Return None if no such plugin exists.

        """

    def get_service(self, interface, query='', minimize='', maximize=''):
        """ Return at most one service that matches the specified query.

        """

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service.

        """
        
    def get_services(self, interface, query='', minimize='', maximize=''):
        """ Return all services that match the specified query.

        """

    def import_symbol(self, symbol_path):
        """ Import the symbol defined by the specified symbol path.

        'symbol_path' is a string containing the path to a symbol through the
        Python package namespace.

        It can be in one of two forms:

        1) 'foo.bar.baz'

           Which is turned into the equivalent of an import statement that
           looks like::

             from foo.bar import baz

           With the value of 'baz' being returned.

        2) 'foo.bar:baz' (i.e. a ':' separating the module from the symbol)

           Which is turned into the equivalent of::

             from foo import bar
             eval('baz', bar.__dict__)

           With the result of the 'eval' being returned.

        The second form is recommended as it allows for nested symbols to be
        retreived, e.g. the symbol path 'foo.bar:baz.bling' becomes::

            from foo import bar
            eval('baz.bling', bar.__dict__)

        The first form is retained for backwards compatability.

        """

    def register_service(self, interface, obj, properties=None):
        """ Register a service.

        Returns a service Id that can be used to retrieve any service
        properties, and to unregister the service.

        """

    def remove_extension_point_listener(self,listener,extension_point_id=None):
        """ Remove a listener for extensions being added/removed.

        Raise a 'ValueError' if the listener does not exist.

        """

    def remove_extension_point(self, extension_point_id):
        """ Remove an extension point.

        Raise an 'UnknownExtensionPoint' exception if no extension point exists
        with the specified Id.

        """

    def run(self):
        """ Run the application.

        The same as::

          application.start()
          application.stop()

        """

    def start(self):
        """ Start the application.

        Return True if the application was started, False if the start was
        vetoed.

        """

    def stop(self):
        """ Stop the application.

        Return True if the application was stopped, False if the stop was
        vetoed.

        """

    def start_plugin(self, plugin=None, plugin_id=None):
        """ Start the specified plugin.

        If a plugin is specified then start it.

        If a plugin Id is specified then use the Id to look up the plugin and
        then start it. If no such plugin exists then a 'SystemError' exception
        is raised.

        """

    def stop_plugin(self, plugin=None, plugin_id=None):
        """ Stop the specified plugin.

        If a plugin is specified then stop it.

        If a plugin Id is specified then use the Id to look up the plugin and
        then stop it. If no such plugin exists then a 'SystemError' exception
        is raised.

        """

    def unregister_service(self, service_id):
        """ Unregister a service.

        """

#### EOF ######################################################################
