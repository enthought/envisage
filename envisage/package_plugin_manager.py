""" A plugin manager that finds plugins in packages on the 'plugin_path'. """


import logging, sys
from fnmatch import fnmatch

from apptools.io import File
from traits.api import Directory, List, on_trait_change, Str

from plugin_manager import PluginManager


logger = logging.getLogger(__name__)


class PackagePluginManager(PluginManager):
    """ A plugin manager that finds plugins in packages on the 'plugin_path'.

    All items in 'plugin_path' are directory names and they are all added to
    'sys.path' (if not already present). Each directory is then searched for
    plugins as follows:-

    a) If the package contains a 'plugins.py' module, then we import it and
    look for a callable 'get_plugins' that takes no arguments and returns
    a list of plugins (i.e. instances that implement 'IPlugin'!).

    b) If the package contains any modules named in the form 'xxx_plugin.py'
    then the module is imported and if it contains a callable 'XXXPlugin' it is
    called with no arguments and it must return a single plugin.

    """

    # Plugin manifest.
    PLUGIN_MANIFEST = 'plugins.py'

    #### 'PackagePluginManager' protocol #######################################

    # An optional list of the Ids of the plugins that are to be excluded by
    # the manager.
    #
    # Each item in the list is actually an 'fnmatch' expression.
    exclude = List(Str)

    # An optional list of the Ids of the plugins that are to be included by
    # the manager (i.e. *only* plugins with Ids in this list will be added to
    # the manager).
    #
    # Each item in the list is actually an 'fnmatch' expression.
    include = List(Str)

    # A list of directories that will be searched to find plugins.
    plugin_path = List(Directory)

    @on_trait_change('plugin_path[]')
    def _plugin_path_changed(self, obj, trait_name, removed, added):
        self._update_sys_dot_path(removed, added)

    #### Protected 'PluginManager' protocol ###################################

    def __plugins_default(self):
        """ Trait initializer. """

        plugins = [
            plugin for plugin in self._harvest_plugins_in_packages()

            if self._is_included(plugin.id) and not self._is_excluded(plugin.id)
        ]

        logger.debug('package plugin manager found plugins <%s>', plugins)

        return plugins

    #### Private protocol #####################################################

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

    def _harvest_plugins_in_package(self, package_name, package_dirname):
        """ Harvest plugins found in the given package. """

        # If the package contains a 'plugins.py' module, then we import it and
        # look for a callable 'get_plugins' that takes no arguments and returns
        # a list of plugins (i.e. instances that implement 'IPlugin'!).
        plugins_module = self._get_plugins_module(package_name)
        if plugins_module is not None:
            factory = getattr(plugins_module, 'get_plugins', None)
            if factory is not None:
                plugins = factory()

        # Otherwise, look for any modules in the form 'xxx_plugin.py' and
        # see if they contain a callable in the form 'XXXPlugin' and if they
        # do, call it with no arguments to get a plugin!
        else:
            plugins = []
            for child in File(package_dirname).children:
                if child.ext == '.py' and child.name.endswith('_plugin'):
                    module = __import__(
                        package_name + '.' + child.name, fromlist=[child.name]
                    )

                    atoms        = child.name.split('_')
                    capitalized  = [atom.capitalize() for atom in atoms]
                    factory_name = ''.join(capitalized)
                    
                    factory = getattr(module, factory_name, None)
                    if factory is not None:
                        plugins.append(factory())
                    
        return plugins

    def _harvest_plugins_in_packages(self):
        """ Harvest plugins found in packages on the plugin path. """

        plugins = []
        for dirname in self.plugin_path:
            for child in File(dirname).children:
                if child.is_package:
                    plugins.extend(
                        self._harvest_plugins_in_package(
                            child.name, child.path
                       ) 
                    )

        return plugins
    
    def _is_excluded(self, plugin_id):
        """ Return True if the plugin Id is excluded.

        If no 'exclude' patterns are specified then this method returns False
        for all plugin Ids.

        """

        if len(self.exclude) == 0:
            return False

        for pattern in self.exclude:
            if fnmatch(plugin_id, pattern):
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
            if fnmatch(plugin_id, pattern):
                return True

        return False

    def _update_sys_dot_path(self, removed, added):
        """ Add/remove the given entries from sys.path. """
        
        for dirname in removed:
            if dirname in sys.path:
                sys.peth.remove(dirname)

        for dirname in added:
            if dirname not in sys.path:
                sys.path.append(dirname)

#### EOF ######################################################################
