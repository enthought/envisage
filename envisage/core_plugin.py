# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The Envisage core plugin. """


# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin, ServiceOffer
from traits.api import List, Instance, on_trait_change, Str


class CorePlugin(Plugin):
    """ The Envisage core plugin.

    The core plugin offers facilities that are generally useful when building
    extensible applications such as adapters, categories and hooks etc. It does
    not contain anything to do with user interfaces!

    The core plugin should be started before any other plugin. It is up to
    the plugin manager to do this.

    """

    # Extension point Ids.
    CATEGORIES       = 'envisage.categories'
    CLASS_LOAD_HOOKS = 'envisage.class_load_hooks'
    PREFERENCES      = 'envisage.preferences'
    SERVICE_OFFERS   = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.core'

    # The plugin's name (suitable for displaying to the user).
    name = 'Core'

    #### Extension points offered by this plugin ##############################

    # Categories are actually implemented via standard 'ClassLoadHooks', but
    # for (hopefully) readability and convenience we have a specific extension
    # point.
    categories = ExtensionPoint(
        List(Instance('envisage.category.Category')),
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
    @on_trait_change('categories_items')
    def _categories_items_changed(self, event):
        """ React to new categories being *added*.

        Note that we don't currently do anything if categories are *removed*.

        """

        self._add_category_class_load_hooks(event.added)

        return

    class_load_hooks = ExtensionPoint(
        List(Instance('envisage.class_load_hook.ClassLoadHook')),
        id   = CLASS_LOAD_HOOKS,
        desc = """

        Class load hooks allow you to be notified when any 'HasTraits' class
        is imported or created.

        See the documentation for 'ClassLoadHook' for more details.

        """
    )
    @on_trait_change('class_load_hooks_items')
    def _class_load_hooks_changed(self, event):
        """ React to new class load hooks being *added*.

        Note that we don't currently do anything if class load hooks are
        *removed*.

        """

        self._connect_class_load_hooks(event.added)

        return

    preferences = ExtensionPoint(
        List(Str),
        id   = PREFERENCES,
        desc = """

        Preferences files allow plugins to contribute default values for
        user preferences. Each contributed string must be the URL of a
        file-like object that contains preferences values.

        e.g.

        'pkgfile://envisage/preferences.ini'

        - this looks for the 'preferences.ini' file in the 'envisage'
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
    @on_trait_change('preferences_items')
    def _preferences_changed(self, event):
        """ React to new preferencess being *added*.

        Note that we don't currently do anything if preferences are *removed*.

        """

        self._load_preferences(event.added)

        return

    service_offers = ExtensionPoint(
        List(ServiceOffer),
        id   = SERVICE_OFFERS,
        desc = """

        Services are simply objects that a plugin wants to make available to
        other plugins. This extension point allows you to offer services
        that are created 'on-demand'.

        e.g.

        my_service_offer = ServiceOffer(
            protocol   = 'acme.IMyService',
            factory    = an_object_or_a_callable_that_creates_one,
            properties = {'a dictionary' : 'that is passed to the factory'}
        )

        See the documentation for 'ServiceOffer' for more details.

        """
    )
    @on_trait_change('service_offers_items')
    def _service_offers_changed(self, event):
        """ React to new service offers being *added*.

        Note that we don't currently do anything if services are *removed* as
        we have no facility to let users of the service know that the offer
        has been retracted.

        """
        for service in event.added:
            self._register_service_offer(service)

        return

    #### Contributions to extension points made by this plugin ################

    # None.

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # Load all contributed preferences files into the application's root
        # preferences node.
        self._load_preferences(self.preferences)

        # Connect all class load hooks.
        self._connect_class_load_hooks(self.class_load_hooks)

        # Add class load hooks for all of the contributed categories. The
        # category will be imported and added when the associated target class
        # is imported/created.
        self._add_category_class_load_hooks(self.categories)

        # Register all service offers.
        #
        # These services are unregistered by the default plugin activation
        # strategy (due to the fact that we store the service ids in this
        # specific trait!).
        self._service_ids = self._register_service_offers(self.service_offers)

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

        # Local imports.
        from .class_load_hook import ClassLoadHook

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

        # Enthought library imports.
        from envisage.resource.api import ResourceManager

        # We add the plugin preferences to the default scope. The default scope
        # is a transient scope which means that (quite nicely ;^) we never
        # save the actual default plugin preference values. They will only get
        # saved if a value has been set in another (persistent) scope - which
        # is exactly what happens in the preferences UI.
        default = self.application.preferences.node('default/')

        # The resource manager is used to find the preferences files.
        resource_manager = ResourceManager()
        for resource_name in preferences:
            f = resource_manager.file(resource_name)
            try:
                default.load(f)

            finally:
                f.close()

        return

    def _register_service_offers(self, service_offers):
        """ Register a list of service offers. """

        return list(map(self._register_service_offer, service_offers))

    def _register_service_offer(self, service_offer):
        """ Register a service offer. """

        service_id = self.application.register_service(
            protocol   = service_offer.protocol,
            obj        = service_offer.factory,
            properties = service_offer.properties
        )

        return service_id

### EOF ######################################################################
