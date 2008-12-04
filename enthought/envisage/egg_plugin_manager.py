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
    """ A plugin manager that gets its plugins from Eggs.

    To declare a plugin (or plugins) in your egg use an entry point in your
    'setup.py' file, e.g.

    [enthought.envisage.plugins]
    acme.foo = acme.foo.foo_plugin:FooPlugin

    The left hand side of the entry point declaration must be the same as the
    'id' trait of the plugin (e.g. the 'FooPlugin' would have its 'id' trait
    set to 'acme.foo'). This allows the plugin manager to filter out plugins
    that are not in the include list (if specified) *without* having to import
    and instantiate them.

    """

    # Entry point Id.
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
            if len(self.include) == 0 or ep.name in self.include:
                klass  = ep.load()
                plugin = klass(application=self.application)
                plugins.append(plugin)

                # Warn if the entry point is an old-style one where the LHS
                # didn't have to be the same as the plugin Id.
                if ep.name != plugin.id:
                    logger.warn(
                        'entry point name <%s> should be the same as the '
                        'plugin id <%s>' % (ep.name, plugin.id)
                    )

        logger.debug('egg plugin manager found plugins <%s>', plugins)

        return plugins

#### EOF ######################################################################
