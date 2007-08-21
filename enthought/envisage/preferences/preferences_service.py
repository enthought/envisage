""" The default preferences service implementation. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Instance, List, Property, Str
from enthought.traits.api import Undefined, implements

# Local imports.
from i_preferences import IPreferences
from i_preferences_service import IPreferencesService

from application_preferences import ApplicationPreferences
from default_preferences import DefaultPreferences
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
    
    # The root node.
    #
    # The root preferences node only contains child nodes - not actual
    # preferences. Each child node represents a single preference *scope*.
    root = Instance(RootPreferences, ())

    #### 'PreferencesService' interface #######################################

    # The scopes (in lookup order).
    scopes = Property(List(IPreferences))

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
    
    def get(self, path, default=None, nodes=[]):
        """ Get the value of the preference at the specified path. """

        # If no nodes were specified explicitly then try the scope nodes in
        # the lookup order. This is the most common way to get preference
        # values.
        if len(nodes) == 0:
            nodes = self.scopes

        # Which still maybe empty if the order contains scope names that don't
        # exist (not that that would be a great idea of course!).
        if len(nodes) == 0:
            value = default

        else:
            for node in nodes:
                value = node.get(path, Undefined)
                if value is not Undefined:
                    break

            else:
                value = default

        return value

    def save(self):
        """ Make sure all scopes persist their preferences. """

        for scope in self.scopes:
            scope.save()

        return

    ###########################################################################
    # 'PreferencesService' interface.
    ###########################################################################

    def _get_scopes(self):
        """ Property getter. """

        return [self.root.children[name] for name in self.lookup_order]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_builtin_scopes(self):
        """ Create the built-in preference scopes. """

        self.root.children['application'] = ApplicationPreferences()
        self.root.children['default']     = DefaultPreferences()

        return

    ###########################################################################
    # Debugging interface.
    ###########################################################################

    def dump(self):
        """ Dump the contents to stdout! """

        for scope in self.scopes:
            scope.dump()

        return
    
#### EOF ######################################################################
