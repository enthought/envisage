""" The Envisage core plugin. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin
from enthought.envisage.resource.api import ResourceManager
from enthought.traits.api import List, Instance, Str


class CorePlugin(Plugin):
    """ The Envisage core plugin.

    The core plugin offers facilities that are generally useful when building
    extensible applications such as adapters, categories and hooks etc. It does
    not contain anything to do with user interfaces!

    """

    # Extension point Ids.
    CLASS_LOAD_HOOKS  = 'enthought.envosage.class_load_hooks'
    PREFERENCES_FILES = 'enthought.envisage.preferences'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id   = 'enthought.envisage.core'

    # The plugin's name (suitable for displaying to the user).
    name = 'Core'

    #### 'CorePlugin' interface ###############################################
    
    # Extension points.
    class_load_hooks = ExtensionPoint(
        List(Instance('enthought.envisage.class_load_hook.ClassLoadHook')),
        id   = CLASS_LOAD_HOOKS,
        desc = """

        This extension point allows you to contribute code that is executed
        when a particular class is loaded (created or imported etc).

        """
    )

    preferences_files = ExtensionPoint(
        List(Str),
        id   = PREFERENCES_FILES,
        desc = """

        This extension point allows you to contribute preferences files. Each
        string must be the URL of a file-like object that contains preferences
        value.

        e.g.

        'pkgfile://enthought.envisage/preferences.ini'

        - this looks for the 'preferences.ini' file in the 'enthought.envisage'
        package.

        'file://C:/tmp/preferences.ini'

        - this looks for the 'preferences.ini' file in 'C:/tmp'

        'http://some.website/preferences.ini'

        - this looks for the 'preferences.ini' document on the 'some.website'
        web site!
        
        """
    )

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # Load all contributed preferences files into the application's root
        # preferences node.
        self._load_preferences_files(self.application.preferences)

        # Connect all class load hooks.
        self._connect_class_load_hooks(self.class_load_hooks)
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _connect_class_load_hooks(self, class_load_hooks):
        """ Connect all class load hooks. """

        for class_load_hook in class_load_hooks:
            class_load_hook.connect()

        return

    def _load_preferences_files(self, preferences):
        """ Load all contributed preferences files into a preferences node. """

        # We add the plugin preferences to the default scope. The default scope
        # is a transient scope which means that (quite nicely ;^) we never
        # save the actual default plugin preference values. They will only get
        # saved if a value has been set in another (persistent) scope - which
        # is exactly what happens in the preferences UI.
        default = preferences.node('default/')

        # The resource manager is used to find the preferences files.
        resource_manager = ResourceManager()
        for resource_name in self.preferences_files:
            f = resource_manager.file(resource_name)
            try:
                default.load(f)

            finally:
                f.close()

        return

### EOF ######################################################################
