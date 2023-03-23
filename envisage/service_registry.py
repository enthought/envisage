# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The service registry. """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import Dict, Event, HasTraits, Int, provides

# Local imports.
from .i_service_registry import IServiceRegistry
from .import_manager import ImportManager

# Logging.
logger = logging.getLogger(__name__)


class NoSuchServiceError(Exception):
    """Raised when a required service is not found."""


@provides(IServiceRegistry)
class ServiceRegistry(HasTraits):
    """The service registry."""

    ####  IServiceRegistry interface ##########################################

    #: An event that is fired when a service is registered.
    registered = Event

    #: An event that is fired when a service is unregistered.
    unregistered = Event

    ####  Private interface ###################################################

    # The services in the registry.
    #
    # { service_id : (protocol_name, obj, properties) }
    #
    # where:
    #
    # 'protocol_name' is the (possible dotted) name of the interface, type or
    # class that the object is registered against.
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

    def get_required_service(
        self, protocol, query="", minimize="", maximize=""
    ):
        """Return the service that matches the specified query.

        Raise a 'NoSuchServiceError' exception if no such service exists.

        """

        service = self.get_service(protocol, query, minimize, maximize)
        if service is None:
            raise NoSuchServiceError(protocol)

        return service

    def get_service(self, protocol, query="", minimize="", maximize=""):
        """Return at most one service that matches the specified query."""

        services = self.get_services(protocol, query, minimize, maximize)
        if len(services) > 0:
            service = services[0]

        else:
            service = None

        return service

    def get_service_from_id(self, service_id):
        """Return the service with the specified id."""

        try:
            protocol, obj, properties = self._services[service_id]

        except KeyError:
            raise ValueError("no service with id <%d>" % service_id)

        return obj

    def get_services(self, protocol, query="", minimize="", maximize=""):
        """Return all services that match the specified query."""

        services = []
        for service_id, (name, obj, properties) in self._services.items():
            if self._get_protocol_name(protocol) == name:
                # If the protocol is a string then we need to import it!
                if isinstance(protocol, str):
                    actual_protocol = ImportManager().import_symbol(protocol)

                # Otherwise, it is an actual protocol, so just use it!
                else:
                    actual_protocol = protocol

                # If the registered service is actually a factory then use it
                # to create the actual object.
                obj = self._resolve_factory(
                    actual_protocol, name, obj, properties, service_id
                )

                # If a query was specified then only add the service if it
                # matches it!
                if len(query) == 0 or self._eval_query(obj, properties, query):
                    services.append(obj)

        # Are we minimizing or maximising anything? If so then sort the list
        # of services by the specified attribute/property.
        if minimize != "":
            services.sort(key=lambda x: getattr(x, minimize))

        elif maximize != "":
            services.sort(key=lambda x: getattr(x, maximize), reverse=True)

        return services

    def get_service_properties(self, service_id):
        """Return the dictionary of properties associated with a service."""

        try:
            protocol, obj, properties = self._services[service_id]
            properties = properties.copy()

        except KeyError:
            raise ValueError("no service with id <%d>" % service_id)

        return properties

    def register_service(self, protocol, obj, properties=None):
        """Register a service."""

        protocol_name = self._get_protocol_name(protocol)

        # Make sure each service gets its own properties dictionary.
        if properties is None:
            properties = {}

        service_id = self._next_service_id()
        self._services[service_id] = (protocol_name, obj, properties)
        self.registered = service_id

        logger.debug("service <%d> registered %s", service_id, protocol_name)

        return service_id

    def set_service_properties(self, service_id, properties):
        """Set the dictionary of properties associated with a service."""

        try:
            protocol, obj, old_properties = self._services[service_id]
            self._services[service_id] = protocol, obj, properties.copy()

        except KeyError:
            raise ValueError("no service with id <%d>" % service_id)

    def unregister_service(self, service_id):
        """Unregister a service."""

        try:
            protocol, obj, properties = self._services.pop(service_id)
            self.unregistered = service_id

            logger.debug("service <%d> unregistered", service_id)

        except KeyError:
            raise ValueError("no service with id <%d>" % service_id)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_namespace(self, service, properties):
        """Create a namespace in which to evaluate a query."""

        namespace = {}
        namespace.update(service.__dict__)
        namespace.update(properties)

        return namespace

    def _eval_query(self, service, properties, query):
        """Evaluate a query over a single service.

        Return True if the service matches the query, otherwise return False.

        """

        namespace = self._create_namespace(service, properties)
        try:
            result = eval(query, namespace)

        except Exception:
            result = False

        return result

    def _get_protocol_name(self, protocol_or_name):
        """Returns the full class name for a protocol."""

        if isinstance(protocol_or_name, str):
            name = protocol_or_name

        else:
            name = "%s.%s" % (
                protocol_or_name.__module__,
                protocol_or_name.__name__,
            )

        return name

    def _is_service_factory(self, protocol, obj):
        """Is the object a factory for services supporting the protocol?"""

        # fixme: Should we have a formal notion of service factory with an
        # appropriate API, or is this good enough? An API might have lifecycle
        # methods to both create and destroy the service?!?

        return not isinstance(obj, protocol)

    def _next_service_id(self):
        """Returns the next service ID."""

        self._service_id += 1

        return self._service_id

    def _resolve_factory(self, protocol, name, obj, properties, service_id):
        """If 'obj' is a factory then use it to create the actual service."""

        # Is the registered service actually a service *factory*?
        if self._is_service_factory(protocol, obj):
            # A service factory is any callable that takes two arguments, the
            # first is the protocol, the second is the (possibly empty)
            # dictionary of properties that were registered with the service.
            #
            # If the factory is specified as a symbol path then import it.
            if isinstance(obj, str):
                obj = ImportManager().import_symbol(obj)

            obj = obj(**properties)

            # The resulting service object replaces the factory in the cache
            # (i.e. the factory will not get called again unless it is
            # unregistered first).
            self._services[service_id] = (name, obj, properties)

        return obj
