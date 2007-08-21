""" A plugin manager that gets its plugins from Eggs. """


# Standard library imports.
import logging, pkg_resources

# Enthought library imports.
from enthought.traits.api import Instance

# Local imports.
from egg_utils import get_entry_points_in_egg_order
from plugin_manager import PluginManager


# Logging.
logger = logging.getLogger(__name__)


class EggPluginManager(PluginManager):
    """ A plugin manager that gets its plugins from Eggs. """

    # Extension point Id.
    PLUGINS = 'enthought.envisage.plugins'
    PREFS   = 'enthought.envisage.preferences'

    #### 'EggPluginManager' interface #########################################
    
    # The working set that contains the eggs that contain the plugins that
    # live in the house that Jack built ;^) By default we use the global
    # working set.
    working_set = Instance(pkg_resources.WorkingSet, pkg_resources.working_set)

    ###########################################################################
    # 'PluginManager' interface.
    ###########################################################################

    #### Trait initializers ###################################################
    
    def _plugins_default(self):
        """ Trait initializer. """

        plugins = []
        for ep in get_entry_points_in_egg_order(self.working_set,self.PLUGINS):
            klass = ep.load()
            plugins.append(klass())

        return plugins

    #### Methods ##############################################################

    def start(self, plugin_context=None):
        """ Start the plugin manager. """

        # Load the plugin preferences...
        self._load_preferences(plugin_context)

        # and the start them.
        super(EggPluginManager, self).start(plugin_context)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _load_preferences(self, plugin_context):
        """ Load all plugin preferences. """

        from enthought.envisage.resource.api import ResourceManager

        # The default preference scope.
        default = plugin_context.preferences.root.node('default')

        resource_manager = ResourceManager()
        for ep in get_entry_points_in_egg_order(self.working_set, self.PREFS):
            # fixme: This is one of the limitations of eggs - we can't have
            # a file name as the RHS of an entry point expression, so we use
            # the LHS (the entry point name). What if we use the dictionary
            # syntax... Hmmm... try explaining that to somebody!
            f = resource_manager.file(ep.name)
            try:
                default.load(f)

            finally:
                f.close()
        
        return
    
#### EOF ######################################################################
