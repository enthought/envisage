""" An extensible, pluggable, application. """


# Standard library imports.
import logging, os

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig
from enthought.envisage.resource.api import ResourceManager
from enthought.preferences.api import IPreferences, PreferencesHelper 
from enthought.preferences.api import ScopedPreferences
from enthought.traits.api import Delegate, Dict, Event, HasTraits, Instance
from enthought.traits.api import Property, Str, VetoableEvent, implements
from enthought.traits.api import on_trait_change

# Local imports.
from i_application import IApplication
from i_extension_provider import IExtensionProvider
from i_extension_registry import IExtensionRegistry
from i_import_manager import IImportManager
from i_plugin_manager import IPluginManager
from i_service_registry import IServiceRegistry

from application_event import ApplicationEvent
from extension_point import ExtensionPoint
from extension_point_connection import ExtensionPointConnection
from import_manager import ImportManager
from service_registry import ServiceRegistry


# Logging.
logger = logging.getLogger(__name__)


class Application(HasTraits):
    """ An extensible, pluggable, application. """

    implements(IApplication)

    #### 'Application' *CLASS* interface ######################################

    # The extension point Id for preferences.
    PREFERENCES = 'enthought.envisage.preferences'
    
    #### 'IApplication' interface #############################################

    # A directory that the application can read and write to at will.
    home = Str

    # The application's globally unique identifier.
    id = Str

    # The root preferences node.
    preferences = Instance(IPreferences)

    #### Events ####

    # Fired when a plugin has been added.
    plugin_added = Delegate('plugin_manager', modify=True)
    
    # Fired when a plugin has been removed.
    plugin_removed = Delegate('plugin_manager', modify=True)

    # Fired when the application is starting.
    starting = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been started.
    started = Event(ApplicationEvent)

    # Fired when the application is stopping.
    stopping = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been stopped.
    stopped = Event(ApplicationEvent)
    
    #### 'Application' interface ##############################################

    # The extension registry.
    extension_registry = Instance(IExtensionRegistry)

    # The import manager.
    import_manager = Instance(IImportManager, factory=ImportManager)

    # The plugin manager (starts and stops plugins etc).
    plugin_manager = Instance(IPluginManager)
    
    # The service registry.
    service_registry = Instance(IServiceRegistry, factory=ServiceRegistry)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, plugins=None, **traits):
        """ Constructor. """

        super(Application, self).__init__(**traits)

        # fixme: We have to initialize the application home here (i.e. we can't
        # wait until the 'home' trait is accessed) because the scoped
        # preferences uses 'ETSConfig.application' home as the default file
        # name.
        self._initialize_application_home()
        
        # This allows the 'ExtensionPoint' trait type to be used as a more
        # convenient way to get the extensions for a given extension point.
        ExtensionPoint.extension_registry = self

        # This allows 'ExtensionPointConnections' to be used as a more
        # convenient way to get the extensions for a given extension point.
        ExtensionPointConnection.extension_registry = self

        # We allow the caller to specify an initial list of plugins, but the
        # list itself is not part of the public API. To add and remove plugins
        # after construction, use the 'add_plugin' and 'remove_plugin' methods
        # respectively.
        if plugins is not None:
            for plugin in plugins:
                self.add_plugin(plugin)

        # This allows instances of 'PreferencesHelper' to be used as a more
        # convenient way to access the preferences.
        #
        # fixme: We need this here to make sure the preferences get
        # initialized, but we have to put them after we have added all plugins!
        # We need to make sure a plugins preferences get loaded when it is
        # added to the application!
        PreferencesHelper.preferences = self.preferences

        return

    def __iter__(self):
        """ Return an iterator over the application's plugins. """

        return iter(self.plugin_manager)
    
    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _home_default(self):
        """ Trait initializer. """

        return ETSConfig.application_home

    def _preferences_default(self):
        """ Trait initializer. """

        preferences = ScopedPreferences()
        self._initialize_preferences(preferences)
        
        return preferences
        
    #### Methods ##############################################################
    
    def add_extension_point_listener(self, listener, extension_point_id=None):
        """ Add a listener for extensions being added/removed.

        """

        self.extension_registry.add_extension_point_listener(
            listener, extension_point_id
        )

        return

    def add_extension_point(self, extension_point):
        """ Add an extension point.

        """

        self.extension_registry.add_extension_point(extension_point)

        return

    def add_plugin(self, plugin):
        """ Add a plugin to the application.

        """

        self.plugin_manager.add_plugin(plugin)

        return
    
    def get_extensions(self, extension_point_id):
        """ Return a list containing all contributions to an extension point.

        """

        return self.extension_registry.get_extensions(extension_point_id)

    def get_extension_point(self, extension_point_id):
        """ Return the extension point with the specified Id.

        """

        return self.extension_registry.get_extension_point(extension_point_id)
        
    def get_extension_points(self):
        """ Return all extension points that have been added to the registry.

        """

        return self.extension_registry.get_extension_points()

    def get_plugin(self, plugin_id):
        """ Return the plugin with the specified Id.

        """

        return self.plugin_manager.get_plugin(plugin_id)

    def get_service(self, interface, query='', minimize='', maximize=''):
        """ Return at most one service that matches the specified query.

        """

        service = self.service_registry.get_service(
            interface, query, minimize, maximize
        )

        return service

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service.

        """

        return self.service_registry.get_service_properties(service_id)
    
    def get_services(self, interface, query='', minimize='', maximize=''):
        """ Return all services that match the specified query.

        """

        services = self.service_registry.get_services(
            interface, query, minimize, maximize
        )

        return services

    def import_symbol(self, symbol_path):
        """ Import the symbol defined by the specified symbol path.
        
        """

        return self.import_manager.import_symbol(symbol_path)

    def register_service(self, interface, obj, properties=None):
        """ Register a service.

        """

        service_id = self.service_registry.register_service(
            interface, obj, properties
        )

        return service_id
    
    def remove_extension_point_listener(self,listener,extension_point_id=None):
        """ Remove a listener for extensions being added/removed.

        """

        self.extension_registry.remove_extension_point_listener(
            listener, extension_point_id
        )

        return

    def remove_extension_point(self, extension_point_id):
        """ Remove an extension point.

        """

        self.extension_registry.remove_extension_point(extension_point_id)

        return

    def remove_plugin(self, plugin):
        """ Remove a plugin from the application.

        """

        self.plugin_manager.remove_plugin(plugin)

        return

    def run(self):
        """ Run the application.

        """

        self.start()
        self.stop()
        
        return

    def set_extensions(self, extension_point_id, extensions):
        """ Set the extensions contributed to an extension point.

        """

        self.extension_registry.set_extensions(extension_point_id, extensions)

        return
    
    def set_service_properties(self, service_id, properties):
        """ Set the dictionary of properties associated with a service. """

        self.service_registry.set_service_properties(service_id, properties)

        return

    def start(self):
        """ Start the application.

        """

        logger.debug('---------- application starting ----------')

        # Lifecycle event.
        self.starting = event = self._create_application_event()
        if not event.veto:
            # Start the plugin manager (this starts all of the manager's
            # plugins).
            self.plugin_manager.start()
            
            # Lifecycle event.
            self.started = self._create_application_event()

            logger.debug('---------- application started ----------')

        else:
            logger.debug('---------- application start vetoed ----------')

        return not event.veto

    def stop(self):
        """ Stop the application.

        """

        logger.debug('---------- application stopping ----------')

        # Lifecycle event.
        self.stopping = event = self._create_application_event()
        if not event.veto:
            # Stop the plugin manager (this stops all of the manager's
            # plugins).
            self.plugin_manager.stop()

            # Save all preferences.
            self.preferences.save()
            
            # Lifecycle event.
            self.stopped = self._create_application_event()

            logger.debug('---------- application stopped ----------')

        else:
            logger.debug('---------- application stop vetoed ----------')
            
        return not event.veto

    def start_plugin(self, plugin=None, plugin_id=None):
        """ Start the specified plugin.

        """

        return self.plugin_manager.start_plugin(plugin, plugin_id)

    def stop_plugin(self, plugin=None, plugin_id=None):
        """ Stop the specified plugin.

        """

        return self.plugin_manager.stop_plugin(plugin, plugin_id)

    def unregister_service(self, service_id):
        """ Unregister a service.

        """

        self.service_registry.unregister_service(service_id)

        return
        
    ###########################################################################
    # 'Application' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _extension_registry_default(self):
        """ Trait initializer. """

        # Do the import here to emphasize that this is just the default
        # extension registry and that the developer is free to override it!
        from plugin_extension_registry import PluginExtensionRegistry

        return PluginExtensionRegistry(application=self)
    
    def _plugin_manager_default(self):
        """ Trait initializer. """

        # Do the import here to emphasize that this is just the default
        # plugin manager and that the developer is free to override it!
        from egg_plugin_manager import EggPluginManager
        
        return EggPluginManager(application=self)

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _plugin_manager_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        if old is not None:
            old.application = None

        if new is not None:
            new.application = self

        return
    
    #### Methods ##############################################################
    
    def _create_application_event(self):
        """ Create an application event. """

        return ApplicationEvent(application=self)

    def _initialize_application_home(self):
        """ Initialize the application home directory. """
        
        ETSConfig.application_home = os.path.join(
            ETSConfig.application_data, self.id
        )

        # Make sure it exists!
        if not os.path.exists(ETSConfig.application_home):
            os.makedirs(ETSConfig.application_home)

        return

    def _initialize_preferences(self, preferences):
        """ Initialize the application's preferences. """

        # We add the plugin preferences to the default scope. The default scope
        # is a transient scope which means that (quite nicely ;^) we never
        # save the actual default plugin preference values. They will only get
        # saved if a value has been set in another (persistent) scope - which
        # is exactly what happens in the preferences UI.
        default = preferences.node('default/')

        # The resource manager is used to find the preferences files.
        resource_manager = ResourceManager()
        for resource_name in self.get_extensions(self.PREFERENCES):
            f = resource_manager.file(resource_name)
            try:
                default.load(f)

            finally:
                f.close()

        return
    
#### EOF ######################################################################
