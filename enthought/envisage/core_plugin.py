""" The Envisage core plugin. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin
from enthought.envisage.resource.api import ResourceManager
from enthought.traits.api import List, Instance, Str

# Local imports.
from category_class_load_hook import CategoryClassLoadHook


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
        List(Instance('enthought.envisage.category.Category')),
        id   = CATEGORIES,
        desc = """

        Traits categories allow you to dynamically extend a Python class with
        extra attributes, methods and events.

        Contributions to this extension point allow you to import categories
        lazily when the class to be extended is imported.

        Contributions to this extension point contain the name of the category
        class that you want to add ('class_name') and the name of the class
        that you want to extend ('target_class_name').

        e.g. To add the 'FooCategory' category to the 'Foo' class::

            Category(
                class_name        = 'foo_category.FooCategory',
                target_class_name = 'foo.Foo'
            )

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

        # Add class load hooks for all of the contributed categories. The
        # category will be imported and added when the associated target class
        # is imported/created.
        self._add_category_class_load_hooks(self.categories)
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_category_class_load_hooks(self, categories):
        """ Add class load hooks for a list of categories. """

        for category in self.categories:
            hook = self._create_category_class_load_hook(category)
            hook.connect()

        return

    def _create_category_class_load_hook(self, category):
        """ Create a category class load hook. """

        category_class_load_hook = CategoryClassLoadHook(
            import_manager      = self.application.import_manager,
            class_name          = category.target_class_name,
            category_class_name = category.class_name,
        )

        return category_class_load_hook
        
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
