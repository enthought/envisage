Services
========

Services are the real "guts" of an Envisage application -- they are the objects
that do the actual work! To get the job done, services obviously need to
interact, and so Envisage provides a way for them to find each other. This is
where the *service registry* comes in.

Don't be fazed by the term *service*. In Envisage it just means any objects
in your application that you want to share between plugins. Services can be
any Python object and do not have to inherit from any Envisage class or even
implement any particular interface!

Service Registry
================

The service registry provides a "Yellow Pages" style mechanism, in that
services are published and looked up by *protocol* meaning *interface*, or
*type*. It is called a "Yellow Pages" mechanism because it is just like looking
up a telephone number in the "Yellow Pages" phone book. You use the
"Yellow Pages" instead of the "White Pages" when you don't know the *name* of
the person you want to call but you do know what *kind* of service you require.
For example, if you have a leaking pipe, you know you need a plumber, so you
pick up your "Yellow Pages", go to the "Plumbers" section and choose one that
seems to fit the bill based on price, location, certification, etc. The service
registry does exactly the same thing as the "Yellow Pages", only with objects,
and it even allows you to publish your own entries for free (unlike the "real"
one)!

In an Envisage application, the service registry is accessed through the
following methods on the IApplication_ interface::

    def get_service(self, protocol, query='', minimimize='', maximize=''):
        """ Return at most one service that matches the specified query.

        """

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service.

        """
        
    def get_services(self, protocol, query='', minimimize='', maximize=''):
        """ Return all services that match the specified query.

        """

    def register_service(self, protocol, obj, properties=None):
        """ Register a service.

        Returns a service ID that can be used to retrieve any service
        properties, and to unregister the service.

        """

    def unregister_service(self, service_id):
        """ Unregister a service.

        """

The easiest way to explain the workings of these methods is to take a look at
some examples, and so to continue our plumber theme, let's assume we have the
following interface and implementation::

    class IPlumber(Interface):
        """ What plumbers do! """

	# The plumber's name.
	name = Str

	# The plumber's location.
	location = Str

	# The price per hour (in say, Estonian Krooni ;^)
	price = Int

	def fix_leaking_pipe(self, pipe):
	    """ Fix a leaking pipe! """

    @provides(IPlumber)
    class Plumber(HasTraits):
        """ An actual plumber implementation! """

	# The plumber's name.
	name = Str

	# The plumber's location.
	location = Str

	# The price per hour (in say, Estonian Krooni ;^)
	price = Int

	def fix_leaking_pipe(self, pipe):
	    """ Fix a leaking pipe! """

	    ... code that actually fixes it! ...

Registering a service
---------------------

To register a service, create an object and call the register_service() method,
passing it the protocol (interface or type) to publish the object under
(for "protocol" think "Yellow Pages" section), and the object to publish. Note
that the object to publish does *not* have to inherit from any particular base
class or implement any special interface -- any arbitrary Python object will
do::

    fred = Plumber(name='fred', location='BH1', price=90)
    fred_id = application.register_service(IPlumber, fred)

Note that each registered service gets assigned an ID that is unique within
the current process. This can be used later
to access its properties, or to unregister it, etc.

You can also associate an arbitrary dictionary of properties with an object
when you register it. These properties, along with the actual attributes of the
service itself, can be used later to lookup the service using the query
mechanism as shown in Section 4.

::

    wilma = Plumber(name='wilma', location='BH6')
    wilma_id = application.register_service(IPlumber, wilma, {'price' : 125})

Note that the symbol name of the protocol can be specified instead of the
actual type or class. Say, for example, that the *IPlumber* interface can be
imported via 'from acme.plumber.api import IPlumber', then the registration
can be written as::

    wilma_id = application.register_service('acme.plumber.api.IPlumber', wilma, {'price' : 125})

This comes in handy when using service factories (see later) to make sure that
implementation classes are imported only when necessary.

Looking up a service
--------------------

Looking up a service is just as easy -- call get_service() specifiying the
protocol of the service required::

    plumber = application.get_service(IPlumber)

Assuming that we have registered both *fred* and *wilma* as in Section 1,
then there is no way of knowing which of those objects would be returned.
The choice of the object returned does *not* necessarily reflect the order in
which they were added, so don't depend on it.

Note that the symbol name of the protocol can be specified instead of the
actual type or class. Say, for example, that the *IPlumber* interface can be
imported via 'from acme.plumber.api import IPlumber', then the service lookup
can be written as::

    plumber = application.get_service('acme.plumber.api.IPlumber')

This comes in handy when using service factories (see later) to make sure that
implementation classes are imported only when necessary.

Looking up a list of services
-----------------------------

You can also look up *all* services of a particular protocol::

    plumbers = application.get_services(IPlumber)

Assuming the registrations in Section 1, this returns a list containing
both *fred* and *wilma*, again in arbitrary order.

Using queries
-------------

The get_service() and get_services() methods both take optional arguments
that allow more control over the selection of an appropriate service. The first
of these is the *query* argument, which is a string containing an arbitrary
Python expression that is evaluated for each service, with the service only
being returned if the expression evaluates to True. The namespace that the
expression is evaluated in is created by first adding each of the service's
attributes, followed by any additional properties that were specified when the
service was registered (i.e., properties take precedence over attributes).

Once again, assuming that we have registered *fred* and *wilma* as in Section
1, let's look at how to use the query mechanism to be more selective
about the plumber(s) we look up.

Find all plumbers whose price is less than 100 Krooni/Hour::

    plumbers = application.get_services(IPlumber, "price < 100")

This query would return a list containing one plumber, *fred*.

Find plumbers named *fred*::

    plumbers = application.get_services(IPlumber, "name == 'fred'")

This query, again (and unsurprisingly), would return a list containing just
*fred*.

Queries can be used with the singular form of the get_service() method too,
in which case only one of the services that matches the query is returned::

    plumber = application.get_service(IPlumber, "price < 200")

This query would return *either* *fred* or *wilma*.	

Using *minimize* and *maximize*
-------------------------------

The *minimize* and *maximize* (optional) arguments to the get_service() and
get_services() methods allow the services returned to be sorted by an
attribute or property in either ascending or descending order respectively.

To find the cheapest plumber::

    cheapest = application.get_service(IPlumber, minimize='price')

Or, if you believe that you get what you pay for, the most expensive::

    most_expensive = application.get_service(IPlumber, maximize='price')

The *minimize* and *maximize* arguments can also be used in conjunction with a
query. For example to find the cheapest plumber in my area::

    cheap_and_local = application.get_service(IPlumber, "location='BH6'", minimize='price')

This query would definitely give the job to *wilma*!

Unregistering a service
-----------------------

When you register a service, Envisage returns a value that uniquely
identifies the service within the current process (i.e., it is not suitable for
persisting to use next time the application is run). To unregister a service,
call the unregister_service() method, passing in the appropriate identifier::

    fred = Plumber(name='fred', location='BH1', price=90)
    fred_id = application.register_service(IPlumber, fred)

    ...

    application.unregister_service(fred_id)

Getting any additional service properties
-----------------------------------------

If you associate an arbitrary dictionary of properties with an object when
you register it, you can retrieve those properties by calling the
get_service_properties() method with the appropriate service identifier::

    wilma = Plumber(name='wilma', location='BH6')
    wilma_id = application.register_service(IPlumber, wilma, {'price':125})
	
    ...

    properties = application.get_service_properties(wilma_id)

This call would return a dictionary containing the following::

    {'price' : 125}

To set the properties for a service that has already been registered, use::

    wilma = Plumber(name='wilma', location='BH6')
    wilma_id = application.register_service(IPlumber, wilma, {'price':125})
	
    ...

    application.set_service_properties(wilma_id, {'price' : 150})

Not however, that in practise, it is more common to use the actual attributes
of a service object for the purposes of querying, but this is useful if you
want additional properties that aren't part of the object's type.

Service Factories
-----------------

Last, but not least, we will look at an important feature of the service
registry, namely, service factories.

Service factories allow a Python callable to be registered in place of an
actual service object. The callable is invoked the first time anybody asks
for a service with the same type that the factory was registered against, and
the object returned by the callable replaces the factory in the registry (so
that the next time it is asked for it is simply returned as normal).


To register a service factory, just register any callable that takes two
arguments. The first is the protocol (type) of the service being requested, and
the second is the (possibly empty) dictionary of properties that were
registered along with the factory, e.g.::

  def wilma_factory(protocol, properties):
      """ A service factory that creates wilma the plumber! """

      return Plumber(name='wilma', location='BH6')

To register the factory, we just use 'application.register_service' as usual::

    wilma_id = application.register_service(IPlumber, wilma_factory, {'price':125})

Now, the first time somebody tries to get any 'IPlumber' service, the factory
is called and the returned plumber object replaces the factory in the registry.

.. _IApplication: https://github.com/enthought/envisage/tree/master/envisage/i_application.py
