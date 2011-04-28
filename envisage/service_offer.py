""" An offer to provide a service. """


# Enthought library imports.
from traits.api import Callable, Dict, Either, HasTraits, Str, Type


class ServiceOffer(HasTraits):
    """ An offer to provide a service. """

    #### 'ServiceOffer' interface #############################################

    # The protocol that the service provides.
    #
    # This can be an actual class or interface, or a string that can be used to
    # import a class or interface.
    #
    # e.g. 'foo.bar.baz.Baz' is turned into 'from foo.bar.baz import Baz'
    protocol = Either(Str, Type)

    # A callable (or a string that can be used to import a callable) that is
    # the factory that creates the actual service object.
    #
    # e.g::
    #
    #   callable(**properties) -> Any
    #
    # e.g. 'foo.bar.baz.Baz' is turned into 'from foo.bar.baz import Baz'
    factory = Either(Str, Callable)

    # An optional set of properties to associate with the service offer.
    #
    # This dictionary is passed as keyword arguments to the factory.
    properties = Dict

#### EOF ######################################################################
