""" The default preferences service implementation. """


# Enthought library imports.
from enthought.traits.api import Any, Dict, HasTraits, Instance, Property, Str
from enthought.traits.api import implements, List

# Local imports.
from i_preferences import IPreferences
from i_preferences_service import IPreferencesService
from preferences import Preferences
from root_preferences import RootPreferences


class PreferencesService(HasTraits):
    """ The default preferences service implementation. """

    implements(IPreferencesService)

    # The default scope lookup order.
    DEFAULT_LOOKUP_ORDER = ['application', 'default']
    
    #### 'IPreferencesService' interface ######################################

    # The scope lookup order. When we are getting a preference value we look
    # in the scopes in this order (each item in the list is the name of a
    # scope).
    lookup_order = List(Str, DEFAULT_LOOKUP_ORDER)

##     # The scopes.
##     scopes = List(IPreferences)
    
    #### 'PreferencesService' interface #######################################

    # The root node.
    #
    # This node only contains child nodes (i.e. it does not contain any
    # preferences). Each child node is a scope ('user', 'system' etc).
    root = Instance(RootPreferences, ())

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(PreferencesService, self).__init__(**traits)

        # Create the 'built-in' preference scopes.
        self._create_builtin_scopes()

        return
    
    ###########################################################################
    # 'IPreferencesService' interface.
    ###########################################################################

    def _scopes_default(self):
        """ Trait initializer. """

        scopes = []
        for scope_name in self.lookup_order:
            scope = Preferences(name=scope_name)
            self.root.children[scope_name] = scope
        
        return scopes
    
    def get(self, path, default=None, nodes=[]):
        """ Get the value of the preferences at the specified path. """

        # If no nodes were specified explicitly then try nodes in the lookup
        # order...
        if len(nodes) == 0:
            nodes = self.root.children.values()#scopes # _get_nodes

        # Which still maybe empty if the order contains scope names that don't
        # exist (not that that would be a great idea of course!).
        if len(nodes) == 0:
            value = default

        else:
            for node in nodes:
                value = node.get(path)
                if value is not None:
                    break

            else:
                value = default

        return value

    def node(self, path):
        """ Return the node at the specified path.

        Create any intermediate nodes if they do not exist.

        """

        if len(path) == 0:
            raise ValueError('empty path')
        
        components = path.split('/')

        node = self._node(components[0])
        if len(components) > 1:
            node = node.node('.'.join(components[1:]))

        return node
    
    ###########################################################################
    # 'IPreferencesService' interface.
    ###########################################################################

##     def _get_nodes(self):
##         """ Return the set of nodes to search through. """

##         return self.scopes
    
##         scopes = [
##             self.root.node(scope_name) for scope_name in self.lookup_order

##             if self.root.has_child(scope_name)
##         ]

##         return scopes

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_builtin_scopes(self):
        """ Create the built-in preference scopes. """
        
        for scope_name in self.DEFAULT_LOOKUP_ORDER:
            self.root.children[scope_name] = Preferences()

        return

#### EOF ######################################################################
