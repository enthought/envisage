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

    #### Trait initializers ###################################################
    
    def _plugins_default(self):
        """ Trait initializer. """
        
        plugins = []
        for ep in get_entry_points_in_egg_order(
            self.working_set, self.PLUGINS
        ):
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

        filenames = []
        for ep in get_entry_points_in_egg_order(
            self.working_set, self.PREFERENCES
        ):
            filenames.append(ep.name)

        if len(filenames) > 0:
            print 'Preference files:', filenames

        # The preferences service.
        preferences = plugin_context.preferences
        
        # The root node.
        root = preferences.root
        print 'root node', root

        # The default scope.
        default = root.node('default')
        print 'default scope', default


        from enthought.envisage.resource.api import ResourceManager
        rm = ResourceManager()
        
        for filename in filenames:
            f = rm.file(filename)
            print 'Loading preferences from', filename
            default.load(f)



        print '-----', preferences.get('acme.ui.workbench.application_name', 'Nah!')
        return
    
#### EOF ######################################################################
