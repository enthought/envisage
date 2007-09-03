""" An extensible, pluggable, application. """


# Standard library imports.
import logging, os

# Enthought library imports.
#
# fixme: The ordering of these imports is critical. We don't use traits UI in
# this module, but it must be imported *before* any 'HasTraits' class whose
# instances might want to have 'edit_traits' called on them.
from enthought.etsconfig.api import ETSConfig
from enthought.envisage.resource.api import ResourceManager
from enthought.preferences.api import IPreferences, PreferencesHelper 
from enthought.preferences.api import ScopedPreferences
from enthought.traits.api import Event, HasTraits, Instance, Property, Str
from enthought.traits.api import VetoableEvent, implements, on_trait_change

# fixme: Just importing the package is enought (see above).
import enthought.traits.ui

# Local imports.
from i_application import IApplication
from i_extension_registry import IExtensionRegistry
from i_import_manager import IImportManager
from i_plugin_manager import IPluginManager
from i_service_registry import IServiceRegistry

from application_event import ApplicationEvent
from egg_plugin_manager import EggPluginManager
from extension_point import ExtensionPoint
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

    # The application's globally unique identifier.
    id = Str

    # Fired when the application is starting.
    starting = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been started.
    started = Event(ApplicationEvent)

    # Fired when the application is stopping.
    stopping = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been stopped.
    stopped = Event(ApplicationEvent)
    
    #### 'Application' interface ##############################################

    # A directory that the application can read and write to at will.
    home = Property(Str)
    
    # The extension registry.
    extension_registry = Instance(IExtensionRegistry)

    # The import manager.
    import_manager = Instance(IImportManager, factory=ImportManager)
    
    # The plugin manager (starts and stops plugins etc).
    plugin_manager = Instance(IPluginManager, factory=EggPluginManager)

    # The preferences service.
    preferences = Instance(IPreferences, factory=ScopedPreferences)
    
    # The service registry.
    service_registry = Instance(IServiceRegistry, factory=ServiceRegistry)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(Application, self).__init__(**traits)

        # The 'application home' is a directory that the application can read
        # and write to at will.
        self._initialize_application_home()
        
        # This allows the 'ExtensionPoint' trait type to be used as a more
        # convenient way to get the extensions for a given extension point.
        ExtensionPoint.extension_registry = self.extension_registry

        # This allows instances of 'PreferencesHelper' to be used as a more
        # convenient way to access the preferences.
        PreferencesHelper.preferences = self.preferences

        return
    
    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _extension_registry_default(self):
        """ Trait initializer. """

        # Do the import here in case the application write doesn't want the
        # default extension registry.
        from extension_registry import ExtensionRegistry
        
        return ExtensionRegistry(application=self)
    
    #### Trait properties #####################################################

    def _get_home(self):
        """ Property getter. """

        return ETSConfig.application_home
    
    #### Methods ##############################################################

    def get_extensions(self, extension_point):
        """ Return a list containing all contributions to an extension point.

        """

        return self.extension_registry.get_extensions(extension_point)
    
    def get_plugin(self, id):
        """ Return the plugin with the specified Id.

        """

        return self.plugin_manager.get_plugin(id)

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

        return self.service_registry.register_service(interface,obj,properties)

    def start(self):
        """ Start the application.

        """

        logger.debug('---------- application starting ----------')

        # Lifecycle event.
        self.starting = event = self._create_application_event()
        if not event.veto:
            # Load any preferences specified via the extension point.
            self._load_preferences()
            
            # Start the plugin manager (this starts all of the manager's
            # plugins).
            self.plugin_manager.start(self)
            
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
            self.plugin_manager.stop(self)

            # Save all preferences.
            self.preferences.save()
            
            # Lifecycle event.
            self.stopped = self._create_application_event()

            logger.debug('---------- application stopped ----------')

        else:
            logger.debug('---------- application stop vetoed ----------')
            
        return not event.veto

    def start_plugin(self, plugin=None, id=None):
        """ Start the specified plugin.

        """

        return self.plugin_manager.start_plugin(self, plugin, id)

    def stop_plugin(self, plugin=None, id=None):
        """ Stop the specified plugin.

        """

        return self.plugin_manager.stop_plugin(self, plugin, id)

    def unregister_service(self, service_id):
        """ Unregister a service.

        """

        self.service_registry.unregister_service(service_id)

        return

    ###########################################################################
    # 'Application' interface.
    ###########################################################################

    def run(self):
        """ Runs the application.

        This does the following (so you don't have to ;^):-

        1) Starts the application
        2) Stops the application

        """

        # Start the application.
        self.start()

        # Stop the application to give all of the plugins a chance to close
        # down cleanly and to do any housekeeping etc.
        self.stop()
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################
    
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

    def _load_preferences(self):
        """ Load any preferences specified via the extension point. """

        # We add the plugin preferences to the default scope. The default scope
        # is a transient scope which means that (quite nicely ;^) we never
        # save the actual default plugin preference values. They will only get
        # saved if a value has been set in another (persistent) scope - which
        # is exactly what happens in the preferences UI.
        default = self.preferences.node('default/')

        resource_manager = ResourceManager()
        for resource_name in self.get_extensions(self.PREFERENCES):
            f = resource_manager.file(resource_name)
            try:
                default.load(f)

            finally:
                f.close()
        
        return
    
#### EOF ######################################################################
