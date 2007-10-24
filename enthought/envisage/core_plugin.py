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
    PREFERENCES_FILES = 'enthought.envisage.preferences'

    #### 'IPlugin' interface ##################################################

    id                = 'enthought.envisage.core'
    name              = 'Core'
    description       = 'The Envisage Core Plugin'
    requires          = []

    #### 'CorePlugin' interface ###############################################
    
    # Extension points.
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
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

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
