""" The service registry. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Dict, HasTraits, Int, Interface, implements

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
    # { service_id : (protocol, obj, properties) }
    #
    # where:
    #
    # 'protocol' is the interface, type or class that the object is registered
    # against.
    #
    # 'obj' is the object that is registered (any old, Python object!).
    #
    # 'properties' is the arbitrary dictionary of properties that were
    # registered with the object.
    _services = Dict

    # The next service Id (service Ids are never persisted between process
    # invocations so this is simply an ever increasing integer!).
    _service_id = Int

    ###########################################################################
    # 'IServiceRegistry' interface.
    ###########################################################################
    
    def get_service(self, protocol, query='', minimize='', maximize=''):
        """ Return at most one service that matches the specified query. """

        services = self.get_services(protocol, query, minimize, maximize)
        if len(services) > 0:
            service = services[0]

        else:
            service = None
            
        return service

    def get_services(self, protocol, query='', minimize='', maximize=''):
        """ Return all services that match the specified query. """

        services = []
        for service_id, (p, obj, properties) in self._services.items():
            if self._get_protocol_name(protocol) == p:
                # If the protocol is an 'Interface' and the registered object
                # does not actually implement the interface then we treat it as
                # a service factory.
                #
                # fixme: Should we have a formal notion of service factory or
                # this is good enough?
                if issubclass(protocol, Interface) and protocol(obj, -1) is -1:
                    # A service factory is any callable that takes the
                    # properties as keyword arguments. This is obviously
                    # designed to make it easy for traits developers so that
                    # that the factory can simply be a class!
                    obj = obj(**properties)
                        
                    # The resulting service object is cached.
                    self._services[service_id] = (p, obj, properties)
                    
                if len(query) == 0 or self._eval_query(obj, properties, query):
                    services.append(obj)

        # Are we minimizing or maximising anything? If so then sort the list
        # of services by the specified attribute/property.
        if minimize != '':
            services.sort(None, lambda x: getattr(x, minimize))

        elif maximize != '':
            services.sort(None, lambda x: getattr(x, maximize), reverse=True)

        return services

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service. """

        try:
            protocol, obj, properties = self._services[service_id]
            properties = properties.copy()
                
        except KeyError:
            raise ValueError('no service with id <%d>' % service_id)
            
        return properties
        
    def register_service(self, protocol, obj, properties=None):
        """ Register a service. """

        protocol_name = self._get_protocol_name(protocol)
        
        # Make sure each service gets its own properties dictionary.
        if properties is None:
            properties = {}

        service_id = self._next_service_id()
        self._services[service_id] = (protocol_name, obj, properties)

        logger.debug('service <%d> registered %s', service_id, protocol_name)
        
        return service_id

    def set_service_properties(self, service_id, properties):
        """ Set the dictionary of properties associated with a service. """

        try:
            protocol, obj, old_properties = self._services[service_id]
            self._services[service_id] = protocol, obj, properties.copy()
                
        except KeyError:
            raise ValueError('no service with id <%d>' % service_id)
           
        return

    def unregister_service(self, service_id):
        """ Unregister a service. """

        try:
            del self._services[service_id]

            logger.debug('service <%d> unregistered', service_id)

        except KeyError:
            raise ValueError('no service with id <%d>' % service_id)
            
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_namespace(self, service, properties):
        """ Create a namespace in which to evaluate a query. """

        namespace = {}
        namespace.update(service.__dict__)
        namespace.update(properties)

        return namespace

    def _eval_query(self, service, properties, query):
        """ Evaluate a query over a single service.

        Return True if the service matches the query, otherwise return False.

        """

        namespace = self._create_namespace(service, properties)
        try:
            result = eval(query, namespace)
            
        except:
            result = False

        return result

    def _get_protocol_name(self, protocol_or_name):
        """ Returns the full class name for a protocol. """

        if isinstance(protocol_or_name, basestring):
            name = protocol_or_name

        else:
            name = '%s.%s' % (
                protocol_or_name.__module__, protocol_or_name.__name__
            )

        return name
    
    def _next_service_id(self):
        """ Returns the next service ID. """

        self._service_id += 1

        return self._service_id
    
#### EOF ######################################################################
