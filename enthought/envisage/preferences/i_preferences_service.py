""" The interface for the preferences service. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface, List, Str

# Local imports.
from i_preferences import IPreferences


class IPreferencesService(Interface):
    """ The interface for the preferences service. """

    # The scope lookup order. When we are getting a preference value we look
    # in the scopes in this order (each item in the list is the name of a
    # scope).
    lookup_order = List(Str)

    # The root node.
    #
    # This node only contains child nodes (i.e. it does not contain any
    # preferences). Each child node is a scope ('user', 'system' etc).
    root = Instance(IPreferences)

    def get(self, path, default=None, nodes=[]):
        """ Get the value of the preferences at the specified path.

        If no nodes were specified explicitly then try nodes in the lookup
        order.

        """

    def set(self, path, value):
        """ Set the value of the preference at the specified path.

        If the path does *not* contain a scope then by default we assume the
        first scope in the lookup order (which in the default case is the
        'application' scope). This seems to be a common case, but we will
        have to see (Eclipse does not have a 'set' method on the service).

        """

    def save(self):
        """ Save all scopes. """

#### EOF ######################################################################
