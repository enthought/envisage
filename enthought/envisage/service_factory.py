""" The declaration of a service factory. """


# Enthought library imports.
from enthought.traits.api import Callable, Dict, Either, HasTraits, Instance
from enthought.traits.api import Interface, Str, Type


class ServiceFactory(HasTraits):
    """ The declaration of a service factory. """
    
    #### 'ServiceFactory' interface ###########################################

    # The protocol that the service provides.
    #
    # This can be an actual class or interface, or the name of the class or
    # interface.
    protocol = Either(Str, Type, Instance(Interface))

    # A callable (or a string that can be used to import a callable) that is
    # the factory that creates the actual service object.
    #
    # e.g.
    #
    #   callable(**properties) -> Any
    #
    factory = Either(Str, Callable)

    # An arbitrary set of properties to associate with the service offer.
    #
    # This dictionary is passed as keyword arguments to the factory.
    properties = Dict
    
    # The service scope.
    #
    # The Envisage core plugin only registers 'application' scope services, but
    # developers are free to create other scopes as they see fit (for example
    # in GUI applications it might be useful to have 'window' scope services).
    scope = Str('application')

#### EOF ######################################################################
