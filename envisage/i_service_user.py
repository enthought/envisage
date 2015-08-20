""" The interface for objects using the 'Service' trait type. """


# Enthought library imports.
from traits.api import Instance, Interface

# Local imports.
from .i_service_registry import IServiceRegistry


class IServiceUser(Interface):
    """ The interface for objects using the 'Service' trait type. """

    # The service registry that the object's services are stored in.
    service_registry = Instance(IServiceRegistry)

#### EOF ######################################################################
