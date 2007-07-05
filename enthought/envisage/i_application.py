""" The application interface. """


# Enthought library imports.
from enthought.traits.api import Event, Interface, VetoableEvent

# Local imports.
from application_event import ApplicationEvent


class IApplication(Interface):
    """ The application interface. """

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

    # Fired when a symbol is imported.
    symbol_imported = Event

    def get_extensions(self, extension_point):
        """ Return a list containing all contributions to an extension point.

        Return an empty list if the extension point does not exist.

        """

    def get_plugin(self, id):
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

        It can be in one of two forms:-

        1) 'foo.bar.baz'

        Which is turned into the equivalent of an import statement that looks
        like:-

        from foo.bar import baz

        With the value of 'baz' being returned.
        
        2) 'foo.bar:baz.bling'

        Which is turned into the equivalent of:-

        from foo import bar
        eval('baz.bling', bar.__dict__)

        With the result of the 'eval' being returned.
        
        """

    def register_service(self, interface, obj, properties=None):
        """ Register a service.

        Returns a service Id that can be used to retrieve any service
        properties, and to unregister the service.

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

    def start_plugin(self, plugin=None, id=None):
        """ Start the specified plugin.

        If a plugin is specified then start it.

        If a plugin Id is specified then use the Id to look up the plugin and
        then start it. If no such plugin exists then a 'SystemError' exception
        is raised.

        """

    def stop_plugin(self, plugin=None, id=None):
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
