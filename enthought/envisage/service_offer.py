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

    # A callable (or a string that can be used to import a callable) that is
    # the factory that creates the actual service object.
    #
    # e.g::
    #
    #   callable(**properties) -> Any
    #
    factory = Either(Str, Callable)

    # An arbitrary set of properties to associate with the service offer.
    #
    # This dictionary is passed as keyword arguments to the factory.
    properties = Dict

#### EOF ######################################################################
