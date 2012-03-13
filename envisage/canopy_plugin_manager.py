""" A plugin manager that gets its plugins from Eggs. """


import logging
from traits.api import Directory, List, Str
from plugin_manager import PluginManager

from egg_basket_plugin_manager import EggBasketPluginManager
from package_plugin_manager import PackagePluginManager


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

    b) If the package contains any modules named in the form 'xxx_plugin.py'
    then the module is imported and if it contains a callable 'XXXPlugin' it is
    called with no arguments and it must return a single plugin.

    """

    # Entry point Id.
    ENVISAGE_PLUGINS_ENTRY_POINT = 'envisage.plugins'

    #### 'CanopyPluginManager' protocol #######################################

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

    ####  Protected 'PluginManager' protocol ##################################

    def __plugins_default(self):
        """ Trait initializer. """


        plugin_managers = [
            EggBasketPluginManager(
                application = self.application,
                exclude     = self.exclude,
                include     = self.include,
                plugin_path = self.plugin_path
            ),

            PackagePluginManager(
                application = self.application,
                exclude     = self.exclude,
                include     = self.include,
                plugin_path = self.plugin_path
            ),
        ]

        plugins = []
        for plugin_manager in plugin_managers:
            # fixme: Using protected protocol!
            plugins.extend(plugin_manager._plugins)

        logger.debug('canopy plugin manager found plugins <%s>', plugins)

        return plugins

#### EOF ######################################################################
