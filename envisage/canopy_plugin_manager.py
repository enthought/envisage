""" A plugin manager that gets its plugins from Eggs. """


import logging, pkg_resources, re, sys
from apptools.io import File
from traits.api import Directory, Instance, List, Str
from egg_utils import add_eggs_on_path, get_entry_points_in_egg_order
from plugin_manager import PluginManager


logger = logging.getLogger(__name__)


class CanopyPluginManager(PluginManager):
    """ A plugin manager that gets its plugins from the following places:-

    1) From any eggs found on the 'plugin_path'.

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

    2) Packages found on the 'plugin_path'.

    All items in 'plugin_path' are directory names and they are all added to
    'sys.path' (if not already present). Each directory is then searched for
    plugins as follows:-

    a) If the package contains a 'plugins.py' module, then we import it and
    look for a callable 'get_plugins' that takes no arguments and returns
    a list of plugins (i.e. instances that implement 'IPlugin'!).
    
    """

    # Entry point Id.
    ENVISAGE_PLUGINS_ENTRY_POINT = 'envisage.plugins'

    #### 'CanopyPluginManager' protocol #######################################

    # An optional list of the Ids of the plugins that are to be excluded by
    # the manager.
    #
    # Each item in the list is actually a regular expression as used by the
    # 're' module.
    exclude = List(Str)

    # An optional list of the Ids of the plugins that are to be included by
    # the manager (i.e. *only* plugins with Ids in this list will be added to
    # the manager).
    #
    # Each item in the list is actually a regular expression as used by the
    # 're' module.
    include = List(Str)

    # A list of directories that will be searched to find plugins.
    plugin_path = List(Directory)
    def _plugin_path_changed(self):
        # Make sure every directory on the plugin path is on 'sys.path'.
        for dirname in self.plugin_path:
            if dirname not in sys.path:
                sys.path.append(dirname)
        
    ####  Protected 'PluginManager' protocol ##################################

    def __plugins_default(self):
        """ Trait initializer. """

        plugins = self._harvest_plugins_in_eggs()
        plugins.extend(self._harvest_plugins_in_packages())
        
        logger.debug('canopy plugin manager found plugins <%s>', plugins)

        return plugins

    #### Private protocol #####################################################

    def _create_plugin_from_entry_point(self, ep):
        """ Create a plugin from an entry point. """

        klass  = ep.load()
        plugin = klass(application=self.application)

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

    def _get_plugins_module(self, package_name):
        """ Import 'plugins.py' from the package with the given name.

        If the package does not exist, or does not contain 'plugins.py' then
        return None.

        """

        try:
            module = __import__(package_name + '.plugins', fromlist=['plugins'])

        except ImportError:
            module = None

        return module
    
    def _harvest_plugins_in_eggs(self):
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
            self._create_plugin_from_entry_point(ep)

            for ep in self._get_plugin_entry_points(plugin_working_set)

            if self._is_included(ep.name) and not self._is_excluded(ep.name)
        ]

        return plugins

    def _harvest_plugins_in_package(self, package_name, dirname):
        """ Harvest plugins found in the given package. """

        # If the package contains a 'plugins.py' module, then we import it and
        # look for a callable 'get_plugins' that takes no arguments and returns
        # a list of plugins (i.e. instances that implement 'IPlugin'!).
        plugins_module = self._get_plugins_module(package_name)
        if plugins_module is not None:
            factory = getattr(plugins_module, 'get_plugins', None)
            if factory is not None:
                plugins = factory()

        else:
            logger.warn('no "plugins.py" module in package <%s>' % package_name)
            plugins = []
            
        return plugins

    def _harvest_plugins_in_packages(self):
        """ Harvest plugins found in packages on the plugin path. """

        plugins = []
        for dirname in self.plugin_path:
            for child in File(dirname).children:
                if child.is_package:
                    plugins_module = self._get_plugins_module(child.name)
                    if plugins_module is not None:
                        factory = getattr(plugins_module, 'get_plugins', None)
                        if factory is not None:
                            plugins.extend(factory())

        return plugins
    
    def _is_excluded(self, plugin_id):
        """ Return True if the plugin Id is excluded.

        If no 'exclude' patterns are specified then this method returns False
        for all plugin Ids.

        """

        if len(self.exclude) == 0:
            return False

        for pattern in self.exclude:
            if re.match(pattern, plugin_id) is not None:
                return True

        return False

    def _is_included(self, plugin_id):
        """ Return True if the plugin Id is included.

        If no 'include' patterns are specified then this method returns True
        for all plugin Ids.

        """

        if len(self.include) == 0:
            return True

        for pattern in self.include:
            if re.match(pattern, plugin_id) is not None:
                return True

        return False

#### EOF ######################################################################
