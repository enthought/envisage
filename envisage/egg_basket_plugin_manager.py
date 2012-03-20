""" A plugin manager that finds plugins in eggs on the 'plugin_path'. """


import logging, pkg_resources, sys

from traits.api import Directory, List, on_trait_change

from egg_utils import add_eggs_on_path, get_entry_points_in_egg_order
from plugin_manager import PluginManager


logger = logging.getLogger(__name__)


class EggBasketPluginManager(PluginManager):
    """ A plugin manager that finds plugins in eggs on the 'plugin_path'.

    To declare a plugin (or plugins) in your egg use an entry point in your
    'setup.py' file, e.g.

    [envisage.plugins]
    acme.foo = acme.foo.foo_plugin:FooPlugin
    acme.foo.fred = acme.foo.fred.fred_plugin:FredPlugin

    The left hand side of the entry point declaration MUST be the same as the
    'id' trait of the plugin (e.g. the 'FooPlugin' would have its 'id' trait
    set to 'acme.foo'). This allows the plugin manager to filter out plugins
    using the 'include' and 'exclude' lists (if specified) *without* having to
    import and instantiate them.

    """

    # Entry point Id.
    ENVISAGE_PLUGINS_ENTRY_POINT = 'envisage.plugins'

    #### 'EggBasketPluginManager' protocol #####################################

    # A list of directories that will be searched to find plugins.
    plugin_path = List(Directory)

    @on_trait_change('plugin_path[]')
    def _plugin_path_changed(self, obj, trait_name, removed, added):
        self._update_sys_dot_path(removed, added)
        self.reset_traits(['_plugins'])
        
    # Protected 'PluginManager' protocol ######################################

    def __plugins_default(self):
        """ Trait initializer. """

        plugins = self._harvest_plugins_in_eggs(self.application)
        
        logger.debug('egg basket plugin manager found plugins <%s>', plugins)

        return plugins

    #### Private protocol #####################################################

    def _create_plugin_from_entry_point(self, ep, application):
        """ Create a plugin from an entry point. """

        klass  = ep.load()
        plugin = klass(application=application)

        # Warn if the entry point is an old-style one where the LHS didn't have
        # to be the same as the plugin Id.
        if ep.name != plugin.id:
            logger.warn(
                'entry point name <%s> should be the same as the '
                'plugin id <%s>' % (ep.name, plugin.id)
            )

        return plugin

    def _get_plugin_entry_points(self, working_set):
        """ Return all plugin entry points in the working set. """

        entry_points = get_entry_points_in_egg_order(
            working_set, self.ENVISAGE_PLUGINS_ENTRY_POINT
        )

        return entry_points

    def _harvest_plugins_in_eggs(self, application):
        """ Harvest plugins found in eggs on the plugin path. """

        # We first add the eggs to a local working set so that when we get
        # the plugin entry points we don't pick up any from other eggs
        # installed on sys.path.
        plugin_working_set = pkg_resources.WorkingSet(self.plugin_path)
        add_eggs_on_path(plugin_working_set, self.plugin_path)

        # We also add the eggs to the global working set as otherwise the
        # plugin classes can't be imported!
        add_eggs_on_path(pkg_resources.working_set, self.plugin_path)

        plugins = [
            self._create_plugin_from_entry_point(ep, application)

            for ep in self._get_plugin_entry_points(plugin_working_set)

            if self._include_plugin(ep.name)
        ]

        return plugins
    
    def _update_sys_dot_path(self, removed, added):
        """ Add/remove the given entries from sys.path. """
        
        for dirname in removed:
            if dirname in sys.path:
                sys.path.remove(dirname)

        for dirname in added:
            if dirname not in sys.path:
                sys.path.append(dirname)

#### EOF ######################################################################
