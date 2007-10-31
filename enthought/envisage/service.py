""" A trait type used to access services. """


# Enthought library imports.
from enthought.traits.api import TraitType, Undefined

# Local imports.
from i_extension_point import IExtensionPoint


class Service(TraitType):
    """ A trait type used to access services. """
    
    #### 'Service' *CLASS* interface ##########################################

    # The application used by *ALL* service traits.
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

        obj = self.application.get_service(
            self._protocol, self._query, self._minimize, self._maximize
        )

        return obj

    def set(self, obj, name, value):
        """ Trait type setter. """

        raise SystemError('Service traits cannot be set')

#### EOF ######################################################################
