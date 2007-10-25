""" The Envisage core plugin. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin
from enthought.envisage.resource.api import ResourceManager
from enthought.traits.api import List, Instance, Str


class CorePlugin(Plugin):
    """ The Envisage core plugin.

    The core plugin offers facilities that are generally useful when building
    extensible applications such as adapters, categories and hooks etc. It does
    not contain anything to do with user interfaces.

    """

    # Extension point Ids.
    ADAPTER_DEFINITIONS = 'enthought.envisage.adapters'
    PREFERENCES_FILES   = 'enthought.envisage.preferences'

    #### 'IPlugin' interface ##################################################

    id                = 'enthought.envisage.core'
    name              = 'Core'
    description       = 'The Envisage Core Plugin'

    #### 'CorePlugin' interface ###############################################
    
    # Extension points.
    adapter_definitions = ExtensionPoint(
        List(Instance('enthought.envisage.adapter_definition')),
        id   = ADAPTER_DEFINITIONS,
        desc = """

        This extension point allows you to contribute adapters. The adapters
        are lazily loaded which in this case means they are loaded when the
        class that they adapt is imported.

        """
    )

    class_load_hook = ExtensionPoint(
        List(Instance('enthought.envisage.class_load_hook.ClassLoadHook')),
        id   = ADAPTER_DEFINITIONS,
        desc = """

        This extension point allows you to contribute adapters. The adapters
        are lazily loaded which in this case means they are loaded when the
        class that they adapt is imported.

        """
    )

    preferences_files = ExtensionPoint(
        List(Str),
        id   = PREFERENCES_FILES,
        desc = """

        This extension point allows you to contribute preferences files.

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

        # Register all contributed adapter factories.
        self._register_adapters(self.adapter_definitions)
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _register_adapters(self, adapter_definitions):
        """ Registers all adapter factories declared in an extension. """

        for adapter_definition in adapter_definitions:
            adapter_definition.connect()

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
