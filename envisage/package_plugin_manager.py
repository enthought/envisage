# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A plugin manager that finds plugins in packages on the 'plugin_path'. """


import logging, sys

from apptools.io import File
from traits.api import Directory, List, on_trait_change

from .plugin_manager import PluginManager


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

    # A list of directories that will be searched to find plugins.
    plugin_path = List(Directory)

    @on_trait_change('plugin_path[]')
    def _plugin_path_changed(self, obj, trait_name, removed, added):
        self._update_sys_dot_path(removed, added)
        self.reset_traits(['_plugins'])

    #### Protected 'PluginManager' protocol ###################################

    def __plugins_default(self):
        """ Trait initializer. """

        plugins = [
            plugin for plugin in self._harvest_plugins_in_packages()

            if self._include_plugin(plugin.id)
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

    # smell: Looooong and ugly!
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
            logger.debug('Looking for plugins in %s' % package_dirname)
            for child in File(package_dirname).children or []:
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
            for child in File(dirname).children or []:
                if child.is_package:
                    plugins.extend(
                        self._harvest_plugins_in_package(
                            child.name, child.path
                       )
                    )

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
