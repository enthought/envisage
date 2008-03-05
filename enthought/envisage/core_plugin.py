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

    The core plugin should be started before any other plugin. It is up to
    the plugin manager to do this.
    
    """

    # Extension point Ids.
    CATEGORIES        = 'enthought.envisage.categories'
    PREFERENCES_FILES = 'enthought.envisage.preferences'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'enthought.envisage.core'

    # The plugin's name (suitable for displaying to the user).
    name = 'Core'

    #### 'CorePlugin' interface ###############################################

    ###########################################################################
    # Extension points offered by this plugin.
    ###########################################################################

    categories = ExtensionPoint(
        List(Instance('enthought.envisage.category_importer.CategoryImporter')),
        id   = CATEGORIES,
        desc = """

        Traits categories allow you to dynamically extend a Python class with
        extra attributes, methods and events.

        Contributions to this extension point contain the name of the class
        you want to add the category to, and the name of the category class.
        The category will not be loaded until the target class is loaded.

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
    # Contributions to extension points made by this plugin.
    ###########################################################################

    # None

    ###########################################################################
    # Services offered by this plugin.
    ###########################################################################

    # None

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # Load all contributed preferences files into the application's root
        # preferences node.
        self._load_preferences_files(self.application.preferences)

        # Add all contributed category importers (the categories are only
        # imported when the class that they extend is imported).
        self._connect_class_load_hooks(self.categories)
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _connect_class_load_hooks(self, class_load_hooks):
        """ Connect a list of class load hooks. """

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
