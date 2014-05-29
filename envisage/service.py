""" A trait type used to access services. """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import TraitType


# Logging.
logger = logging.getLogger(__name__)


class Service(TraitType):
    """ A trait type used to access services.

    Note that this is a trait *type* and hence does *NOT* have traits itself
    (i.e. it does *not* inherit from 'HasTraits').

    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(
        self, protocol=None, query='', minimize='', maximize='', **metadata
    ):
        """ Constructor. """

        super(Service, self).__init__(**metadata)

        # The protocol that the service must provide.
        self._protocol = protocol

        # The optional query.
        self._query = query

        # The optional name of the trait/property to minimize.
        self._minimize = minimize

        # The optional name of the trait/property to maximize.
        self._maximize = maximize

        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, trait_name):
        """ Trait type getter. """

        service_registry = self._get_service_registry(obj)


        obj = service_registry.get_service(
            self._protocol, self._query, self._minimize, self._maximize
        )

        return obj

    def set(self, obj, name, value):
        """ Trait type setter. """

        raise SystemError('Service traits cannot be set')

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_service_registry(self, obj):
        """ Return the service registry in effect for an object. """

        service_registry = getattr(obj, 'service_registry', None)
        if service_registry is None:
            raise ValueError(
                'The "Service" trait type can only be used within objects ' \
                'that have a reference to a service registry via their ' \
                '"service_registry" trait. \n' \
                'Object %s\nService protocol %s' % (obj, self._protocol)
            )

        return service_registry

#### EOF ######################################################################
