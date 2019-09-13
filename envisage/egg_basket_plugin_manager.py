# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A plugin manager that finds plugins in eggs on the 'plugin_path'. """


import logging, pkg_resources, sys
import traceback

from traits.api import Callable, Directory, List, on_trait_change

from .egg_utils import add_eggs_on_path, get_entry_points_in_egg_order
from .plugin_manager import PluginManager


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

    # If a plugin cannot be loaded for any reason, this callable is called
    # with the following arguments: entry_point, exception.
    on_broken_plugin = Callable

    def _on_broken_plugin_default(self):
        def handle_broken_plugin(entry_point, exc):
            raise exc
        return handle_broken_plugin

    # If a distribution cannot be loaded for any reason
    # (mainly VersionConflict), this callable is called with the following
    # arguments: distribution, exception.
    on_broken_distribution = Callable

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
            logger.warning(
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
        add_eggs_on_path(plugin_working_set, self.plugin_path,
                         self._handle_broken_distributions)

        # We also add the eggs to the global working set as otherwise the
        # plugin classes can't be imported!
        add_eggs_on_path(pkg_resources.working_set, self.plugin_path,
                         self._handle_broken_distributions)

        plugins = []
        for entry_point in self._get_plugin_entry_points(plugin_working_set):
            if self._include_plugin(entry_point.name):
                try:
                    plugin = self._create_plugin_from_entry_point(entry_point,
                                                                  application)
                    plugins.append(plugin)
                except Exception as exc:
                    exc_tb = traceback.format_exc()
                    msg = 'Error loading plugin: %s (from %s)\n%s'\
                        %(entry_point.name, entry_point.dist.location, exc_tb)
                    logger.error(msg)
                    self.on_broken_plugin(entry_point, exc)

        return plugins

    def _handle_broken_distributions(self, errors):
        logger.error('Error loading distributions: %s', errors)
        if self.on_broken_distribution is None:
            raise SystemError('Cannot find eggs %s' % errors)
        else:
            for dist, exc in errors.items():
                self.on_broken_distribution(dist, exc)

    def _update_sys_dot_path(self, removed, added):
        """ Add/remove the given entries from sys.path. """

        for dirname in removed:
            if dirname in sys.path:
                sys.path.remove(dirname)

        for dirname in added:
            if dirname not in sys.path:
                sys.path.append(dirname)

#### EOF ######################################################################
