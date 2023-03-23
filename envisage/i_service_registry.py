# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The service registry interface. """


# Enthought library imports.
from traits.api import Event, Interface


class IServiceRegistry(Interface):
    """The service registry interface.

    The service registry provides a 'Yellow Pages' style mechanism, in that
    services are published and looked up by protocol (meaning, *interface*,
    *type*, or *class* (for old-style classes!). It is called a 'Yellow Pages'
    mechanism because it is just like looking up a telephone number in the
    'Yellow Pages' phone book. You use the 'Yellow Pages' instead of the
    'White Pages' when you don't know the *name* of the person you want to
    call but you do know what *kind* of service you require. For example, if
    you have a leaking pipe, you know you need a plumber, so you pick up your
    'Yellow Pages', go to the 'Plumbers' section and choose one that seems to
    fit the bill based on price, location, certification, etc. The service
    registry does exactly the same thing as the 'Yellow Pages', only with
    objects, and it even allows you to publish your own entries for free
    (unlike the *real* one)!

    """

    # An event that is fired when a service is registered.
    registered = Event

    # An event that is fired when a service is unregistered.
    unregistered = Event

    def get_service(self, protocol, query="", minimize="", maximize=""):
        """Return at most one service that matches the specified query.

        The protocol can be an actual class or interface, or the *name* of a
        class or interface in the form '<module_name>.<class_name>'.

        Return None if no such service is found.

        If no query is specified then a service that provides the specified
        protocol is returned (if one exists).

        NOTE: If more than one service exists that match the criteria then
        Don't try to guess *which* one it will return - it is random!

        """

    def get_service_from_id(self, service_id):
        """Return the service with the specified id.

        If no such service exists a 'ValueError' exception is raised.

        """

    def get_services(self, protocol, query="", minimize="", maximize=""):
        """Return all services that match the specified query.

        The protocol can be an actual class or interface, or the *name* of a
        class or interface in the form '<module_name>.<class_name>'.

        If no services match the query, then an empty list is returned.

        If no query is specified then all services that provide the specified
        protocol are returned (if any exist).

        """

    def get_service_properties(self, service_id):
        """Return the dictionary of properties associated with a service.

        If no such service exists a 'ValueError' exception is raised.

        The properties returned are 'live' i.e. changing them immediately
        changes the service registration.

        """

    def register_service(self, protocol, obj, properties=None):
        """Register a service.

        The protocol can be an actual class or interface, or the *name* of a
        class or interface in the form::

            'foo.bar.baz'

        Which is turned into the equivalent of an import statement that
        looks like::

            from foo.bar import baz

        Return a service Id that can be used to unregister the service and to
        get/set any service properties.

        If 'obj' does not implement the specified protocol then it is treated
        as a 'service factory' that will be called the first time a service of
        the appropriate type is requested. A 'service factory' is simply a
        callable that takes the properties specified here as keyword arguments
        and returns an object. For *really* lazy loading, the factory can also
        be specified as a string which is used to import the callable.

        """

    def set_service_properties(self, service_id, properties):
        """Set the dictionary of properties associated with a service.

        If no such service exists a 'ValueError' exception is raised.

        """

    def unregister_service(self, service_id):
        """Unregister a service.

        If no such service exists a 'ValueError' exception is raised.

        """
