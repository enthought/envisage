""" An offer to provide a service. """


# Enthought library imports.
from enthought.traits.api import Callable, Dict, Either, HasTraits, Instance
from enthought.traits.api import Interface, Str, Type


class ServiceOffer(HasTraits):
    """ An offer to provide a service. """
    
    #### 'ServiceOffer' interface #############################################

    # The protocol that the service provides.
    #
    # This can be an actual class or interface, or the name of the class or
    # interface.
    protocol = Either(Str, Type, Instance(Interface))

    # The factory that will create the service.
    #
    # This is any callable with the following signature:-
    #
    #   callable(protocol, properties) -> Any
    #
    # Where 'protocol' is the type of service requested and 'properties' is a
    # dictionary of properties.
    factory = Either(Str, Callable)

    # An arbitrary set of properties to associate with the service offer.
    #
    # This dictionary is passed as keyword arguments to the factory.
    properties = Dict
    
    # The service scope.
    #
    # The Envisage core plugin only registers 'application' scope services.
    # Developers are free to create other scopes as they see fit.
    scope = Str('application')

#### EOF ######################################################################
