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
    
    # The working set that contains the eggs that contain the plugins that
    # live in the house that Jack built ;^) By default we use the global
    # working set.
    working_set = Instance(pkg_resources.WorkingSet, pkg_resources.working_set)

    # An optional list of the Ids of the plugins that are to be included by
    # the manager (i.e. *only* plugins with Ids in this list will be added to
    # the manager).
    include = List(Str)
    
    ###########################################################################
    # Protected 'PluginManager' interface.
    ###########################################################################

    def __plugins_default(self):
        """ Trait initializer. """

        plugins = []
        for ep in get_entry_points_in_egg_order(self.working_set,self.PLUGINS):
            klass  = ep.load()
            plugin = klass(application=self.application)

            if len(self.include) == 0 or plugin.id in self.include:
                plugins.append(plugin)

        logger.debug('egg plugin manager found plugins <%s>', plugins)
        
        return plugins

#### EOF ######################################################################
