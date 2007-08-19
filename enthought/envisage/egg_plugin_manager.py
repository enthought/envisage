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
    PLUGINS     = 'enthought.envisage.plugins'
    PREFERENCES = 'enthought.envisage.preferences'

    #### 'EggPluginManager' interface #########################################
    
    # The working set that contains the eggs that contain the plugins that
    # live in the house that Jack built ;^) By default we use the global
    # working set.
    working_set = Instance(pkg_resources.WorkingSet, pkg_resources.working_set)

    ###########################################################################
    # 'PluginManager' interface.
    ###########################################################################
 
    def _plugins_default(self):
        """ Initializer. """
        
        plugins = []
        for ep in get_entry_points_in_egg_order(
            self.working_set,self.PLUGINS
        ):
            klass = ep.load()
            plugins.append(klass())

        filenames = []
        for ep in get_entry_points_in_egg_order(
            self.working_set,self.PREFERENCES
        ):
            filenames.append(ep.name)

        if len(filenames) > 0:
            print 'Preference files:', filenames
        
        return plugins
        
#### EOF ######################################################################
