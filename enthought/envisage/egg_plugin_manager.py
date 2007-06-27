""" A plugin manager that gets its plugins from Eggs. """


# Standard library imports.
import logging, pkg_resources

# Enthought library imports.
from enthought.traits.api import Instance, List, Str

# Local imports.
from egg_utils import get_entry_points_in_egg_order
from plugin_manager import PluginManager


# Logging.
logger = logging.getLogger(__name__)


class EggPluginManager(PluginManager):
    """ A plugin manager that gets its plugins from Eggs. """

    # Extension point Id.
    PLUGINS = 'enthought.envisage.plugins'

    #### 'EggPluginManager' interface #########################################

    # A list of directories that contain (or at least, *may* contain) plugin
    # eggs.
    plugin_path = List(Str)
    
    # The working set that contains the eggs that contain the plugins that
    # live in the house that Jack built ;^) By default we use the global
    # working set.
    working_set = Instance(pkg_resources.WorkingSet, pkg_resources.working_set)

    ###########################################################################
    # 'PluginManager' interface.
    ###########################################################################
 
    def _plugins_default(self):
        """ Initializer. """

        self._add_eggs_to_working_set(self.working_set, self.plugin_path)
        
        plugins = []
        for ep in get_entry_points_in_egg_order(self.working_set,self.PLUGINS):
            klass = ep.load()
            plugins.append(klass())

        return plugins

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_eggs_to_working_set(self, working_set, plugin_path):
        """ Add all eggs found in the specified directory list. """

        # 'find_plugins' identifies those distributions that *could* be added
        # to the working set without version conflicts or missing requirements.
        distributions, errors = working_set.find_plugins(
            pkg_resources.Environment(plugin_path)
        )

        logger.debug('found eggs %s', distributions)
        
        if len(errors) > 0:
            logger.error('finding eggs %s', errors)

        # 'add' adds the distributions to the working set!
        map(working_set.add, distributions)

        return
        
#### EOF ######################################################################
