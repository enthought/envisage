""" A plugin manager that gets its plugins from Eggs. """


import logging
from traits.api import Directory, List, Str

from composite_plugin_manager import CompositePluginManager
from egg_basket_plugin_manager import EggBasketPluginManager
from package_plugin_manager import PackagePluginManager
from plugin_manager import PluginManager


logger = logging.getLogger(__name__)


class CanopyPluginManager(CompositePluginManager):
    """ A plugin manager that gets its plugins from the following places:-

    1) An (optional) list of plugin instances passed at construction time.

    e.g::

        plugin_manager = CanopyPluginManager(plugins=[MyPlugin(), YourPlugin()])
    
    2) From any eggs found on the 'plugin_path'.

    To declare a plugin (or plugins) in your egg use an entry point in your
    'setup.py' file, e.g::

    [envisage.plugins]
    acme.foo = acme.foo.foo_plugin:FooPlugin
    acme.foo.fred = acme.foo.fred.fred_plugin:FredPlugin

    The left hand side of the entry point declaration MUST be the same as the
    'id' trait of the plugin (e.g. the 'FooPlugin' would have its 'id' trait
    set to 'acme.foo'). This allows the plugin manager to filter out plugins
    using the 'include' and 'exclude' lists (if specified) *without* having to
    import and instantiate them.

    3) Packages found on the 'plugin_path'.

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

    #### 'object' protocol #####################################################

    def __init__(self, plugins=None, **traits):
        """ Constructor. """

        super(CanopyPluginManager, self).__init__(**traits)

        self.plugin_managers = [
            self._create_explicit_plugin_manager(plugins or []),
            self._create_egg_basket_plugin_manager(),
            self._create_package_plugin_manager()
        ]

        return

    #### Private protocol ######################################################

    def _create_egg_basket_plugin_manager(self):
        """ Factory method for the 'Egg Basket' plugin manager. """

        egg_basket_plugin_manager = EggBasketPluginManager(
            exclude     = self.exclude,
            include     = self.include,
            plugin_path = self.plugin_path
        )

        return egg_basket_plugin_manager

    def _create_explicit_plugin_manager(self, plugins):
        """ Factory method for the explicit plugin manager. """

        plugin_manager = PluginManager(
            exclude = self.exclude,
            include = self.include,
            plugins = plugins
        )

        return plugin_manager

    def _create_package_plugin_manager(self):
        """ Factory method for the 'Package' plugin manager. """

        package_plugin_manager = PackagePluginManager(
            exclude     = self.exclude,
            include     = self.include,
            plugin_path = self.plugin_path
        )

        return package_plugin_manager

#### EOF #######################################################################
