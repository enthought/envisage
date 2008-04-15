""" A trait type used to access services. """


# Enthought library imports.
from enthought.traits.api import TraitType


class Service(TraitType):
    """ A trait type used to access services.
    
    Note that this is a trait *type* and hence does *NOT* have traits itself
    (i.e. it does *not* inherit from 'HasTraits').

    """
    
    #### 'Service' *CLASS* interface ##########################################

    # The application used by *ALL* service traits.
    #
    # fixme: This sneaks a global reference to the application which means that
    # you can't have more than one application per process. That may sound a
    # bit weird, but I can see that it could come in handy. Maybe it would
    # also be worth renaming 'Applicaton' to 'Environment', 'Context' or
    # 'Capsule' or something to get across the point that it is just a little
    # world that plugins can plugio into).
    #
    # If we restrict the scope of usage of this trait type to plugins *only*
    # then we can find the application via the plugins themselves.
    application = None # Instance(IApplication)
    
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

        obj = self._get_service_registry(obj).get_service(
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

##         service_registry = getattr(obj, 'service_registry', None)
        service_registry = self.application
        if service_registry is None:
            raise 'The "Service" trait type can only be used within objects ' \
                  'that have a reference to a service registry via their ' \
                  '"service_registry" trait.' \
                  'Service protocol <%s>' % self._protocol

        return service_registry

#### EOF ######################################################################
