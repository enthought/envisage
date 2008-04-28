""" The Envisage core plugin. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin, ServiceFactory
from enthought.envisage.resource.api import ResourceManager
from enthought.traits.api import List, Instance, Str

# Local imports.
from class_load_hook import ClassLoadHook


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
    CLASS_LOAD_HOOKS  = 'enthought.envisage.class_load_hooks'    
    PREFERENCES       = 'enthought.envisage.preferences'
    SERVICE_FACTORIES = 'enthought.envisage.service_factories'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'enthought.envisage.core'

    # The plugin's name (suitable for displaying to the user).
    name = 'Core'

    #### Extension points offered by this plugin ##############################

    # Categories are actually implemented via standard 'ClassLoadHooks', but
    # for (hopefully) readability and convenience we have a specific extension
    # point.
    categories = ExtensionPoint(
        List(Instance('enthought.envisage.category.Category')),
        id   = CATEGORIES,
        desc = """

        Traits categories allow you to dynamically extend a Python class with
        extra attributes, methods and events.

        Contributions to this extension point allow you to import categories
        *lazily* when the class to be extended is imported or created. Each
        contribution contains the name of the category class that you want to
        add (the 'class_name') and the name of the class that you want to
        extend (the 'target_class_name').

        e.g. To add the 'FooCategory' category to the 'Foo' class::

            Category(
                class_name        = 'foo_category.FooCategory',
                target_class_name = 'foo.Foo'
            )

        """
    )
    
    class_load_hooks = ExtensionPoint(
        List(Instance('enthought.envisage.class_load_hook.ClassLoadHook')),
        id   = CLASS_LOAD_HOOKS,
        desc = """

        Class load hooks allow you to be notified when any 'HasTraits' class
        is imported or created.

        See the documentation for 'ClassLoadHook' for more details.

        """
    )
    
    preferences = ExtensionPoint(
        List(Str),
        id   = PREFERENCES,
        desc = """

        Preferences files allow plugins to contribute default values for
        user preferences. Each contributed string must be the URL of a
        file-like object that contains preferences values.

        e.g.

        'pkgfile://enthought.envisage/preferences.ini'

        - this looks for the 'preferences.ini' file in the 'enthought.envisage'
        package.

        'file://C:/tmp/preferences.ini'

        - this looks for the 'preferences.ini' file in 'C:/tmp'

        'http://some.website/preferences.ini'

        - this looks for the 'preferences.ini' document on the 'some.website'
        web site!

        The files themselves are parsed using the excellent 'ConfigObj'
        package. For detailed documentation please go to:-

        http://www.voidspace.org.uk/python/configobj.html

        """
    )

    service_factories = ExtensionPoint(
        List(ServiceFactory),
        id   = SERVICE_FACTORIES,
        desc = """

        Services are simply objects that a plugin wants to make available to
        other plugins. This extension point allows you to contribute factories
        (i.e. callables) that create your service objects 'on-demand'.

        e.g.

        my_service_factory = ServiceFactory(
            protocol   = 'acme.IMyService',
            factory    = an_object_or_a_callable_that_creates_one,
            properties = {'a dictionary' : 'that is passed to the factory'}
        )

        """
    )

    #### Contributions to extension points made by this plugin ################

    # None.

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # Load all contributed preferences files into the application's root
        # preferences node.
        self._load_preferences(self.application.preferences)
        
        # Connect all class load hooks.
        self._connect_class_load_hooks(self.class_load_hooks)
        
        # Add class load hooks for all of the contributed categories. The
        # category will be imported and added when the associated target class
        # is imported/created.
        self._add_category_class_load_hooks(self.categories)

        # Register all application-scope service factories.
        #
        # These services are unregistered by the default plugin activation
        # strategy (due to the fact that we store the service ids in this
        # specific trait!).
        self._service_ids = self._register_service_factories(
            self.service_factories
        )

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_category_class_load_hooks(self, categories):
        """ Add class load hooks for a list of categories. """

        for category in categories:
            class_load_hook = self._create_category_class_load_hook(category)
            class_load_hook.connect()

        return

    def _connect_class_load_hooks(self, class_load_hooks):
        """ Connect all class load hooks. """

        for class_load_hook in class_load_hooks:
            class_load_hook.connect()

        return
    
    def _create_category_class_load_hook(self, category):
        """ Create a category class load hook. """

        def import_and_add_category(cls):
            """ Import a category and add it to a class.

            This is a closure that binds 'self' and 'category'.

            """

            category_cls = self.application.import_symbol(category.class_name)
            cls.add_trait_category(category_cls)

            return

        category_class_load_hook = ClassLoadHook(
            class_name = category.target_class_name,
            on_load    = import_and_add_category
        )

        return category_class_load_hook
        
    def _load_preferences(self, preferences):
        """ Load all contributed preferences into a preferences node. """

        # We add the plugin preferences to the default scope. The default scope
        # is a transient scope which means that (quite nicely ;^) we never
        # save the actual default plugin preference values. They will only get
        # saved if a value has been set in another (persistent) scope - which
        # is exactly what happens in the preferences UI.
        default = preferences.node('default/')

        # The resource manager is used to find the preferences files.
        resource_manager = ResourceManager()
        for resource_name in self.preferences:
            f = resource_manager.file(resource_name)
            try:
                default.load(f)

            finally:
                f.close()

        return

    def _register_service_factories(self, service_factories):
        """ Regoster all application-scope service factories. """

        service_ids = []
        for service_factory in service_factories:
            if service_factory.scope == 'application':
                service_id = self._register_service_factory(service_factory)
                service_ids.append(service_id)
                
        return service_ids

    def _register_service_factory(self, service_factory):
        """ Register a service factory. """

        service_id = self.application.register_service(
            protocol   = service_factory.protocol,
            obj        = service_factory.factory,
            properties = service_factory.properties
        )

        return service_id

### EOF ######################################################################
