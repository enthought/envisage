""" The service registry. """


# Standard library imports.
import logging, random

# Enthought library imports.
from enthought.traits.api import Dict, HasTraits, Int, implements

# Local imports.
from i_service_registry import IServiceRegistry


# Logging.
logger = logging.getLogger(__name__)


class ServiceRegistry(HasTraits):
    """ The service registry. """

    implements(IServiceRegistry)

    ####  Private interface ###################################################
    
    # The services in the registry.
    #
    # { service_id : (interface, obj, properties) }
    _services = Dict

    # The next service Id (service Ids are never persisted between process
    # invocations so this is simply an ever increasing integer!).
    _service_id = Int

    ###########################################################################
    # 'IServiceRegistry' interface.
    ###########################################################################
    
    def get_service(self, interface, query=None):
        """ Return at most one service that matches the specified query. """

        services = self.get_services(interface, query)

        # We use a random choice here (as opposed to just returning the first
        # appropriate service) to make sure that people don't rely on the
        # ordering of services in the registry.
        if len(services) > 0:
            service = random.choice(services)

        else:
            service = None

        return service

    def get_service_properties(self, service_id):
        """ Return the dicitonary of properties associated with a service. """

        try:
            interface, obj, properties = self._services[service_id]

        except KeyError:
            raise ValueError('no service with id [%d]' % service_id)

        return properties
        
    def get_services(self, interface, query=None):
        """ Return all services that match the specified query. """

        services = []
        for service_id, (i, obj, properties) in self._services.items():
            if interface == i:
                # If the object does not actually implement the interface then
                # we treat it a service factory.
                #
                # fixme: Should we have a formal notion of service factory or
                # this is good enough?
                if interface(obj, None) is None:
                    # A service factory is any callable that takes the
                    # properties as keyword arguments. This is obviously
                    # designed to make it easy for traits developers so that
                    # the factory can simply be a class!
                    obj = obj(**properties)

                    # The resulting service object is cached.
                    self._services[service_id] = (i, obj, properties)
                    
                if query is None or self._eval_query(obj, properties, query):
                    services.append(obj)

        return services

    def register_service(self, interface, obj, properties=None):
        """ Register a service. """

        # Make sure each service gets its own properties dictionary.
        properties = properties or {}

        service_id = self._next_service_id()
        self._services[service_id] = (interface, obj, properties)

        logger.debug('service [%d] registered [%s]', service_id, interface)
        
        return service_id

    def unregister_service(self, service_id):
        """ Unregister a service. """

        try:
            del self._services[service_id]

            logger.debug('service [%d] unregistered', service_id)

        except KeyError:
            raise ValueError('no service with id [%d]' % service_id)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_namespace(self, service, properties):
        """ Creates a namespace in which to evaluate a query. """

        namespace = {}
        namespace.update(service.__dict__)
        namespace.update(properties)

        return namespace

    def _eval_query(self, service, properties, query):
        """ Evaluates a query over a single service.

        Returns True if the service matches the query, otherwise returns False.

        """

        namespace = self._create_namespace(service, properties)
        try:
            result = eval(query, namespace)
            
        except:
            result = False

        return result
    
    def _next_service_id(self):
        """ Returns the next service ID. """

        self._service_id += 1

        return self._service_id
    
#### EOF ######################################################################
