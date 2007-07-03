""" The service registry interface. """


# Enthought library imports.
from enthought.traits.api import Interface


class IServiceRegistry(Interface):
    """ The service registry interface. """

    def get_service(self, interface, query='', minimize='', maximize=''):
        """ Return at most one service that matches the specified query.

        Return None if no such service is found.

        If no query is specified then a service that provides the specified
        interface is returned (if one exists).
        
        NOTE: If more than one service exists that match the criteria then
        Don't try to guess *which* one it will return - it is random!

        """

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service.

        If no such service exists a 'ValueError' exception is raised.

        The properties returned are 'live' i.e. changing them immediately
        reflects the service registration.
        
        """

    def get_services(self, interface, query='', minimize='', maximize=''):
        """ Return all services that match the specified query.

        If no services match the query, then an empty list is returned.

        If no query is specified then all services that provide the specified
        interface are returned (if any exist).

        """
        
    def register_service(self, interface, obj, properties=None):
        """ Register a service.

        Returns a service Id that can be used to retrieve any service
        properties, and to unregister the service.
        
        """
        
    def unregister_service(self, service_id):
        """ Unregister a service.

        If no such service exists a 'ValueError' exception is raised.

        """

#### EOF ######################################################################
