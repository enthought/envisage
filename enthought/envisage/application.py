""" An extensible, pluggable, application. """


# Standard library imports.
import logging

# Enthought library imports.
#
# fixme: The ordering of these imports is critical. We don't use traits UI in
# this module, but it must be imported *before* any 'HasTraits' class whose
# instances might want to have 'edit_traits' called on them.
from enthought.traits.api import Event, HasTraits, Instance, Str, VetoableEvent
from enthought.traits.api import implements, on_trait_change

# fixme: Just importing the package is enought (see above).
import enthought.traits.ui

# Local imports.
from i_application import IApplication
from i_extension_registry import IExtensionRegistry
from i_import_manager import IImportManager
from i_plugin_manager import IPluginManager
from i_service_registry import IServiceRegistry

from application_event import ApplicationEvent
from egg_extension_registry import EggExtensionRegistry
from egg_plugin_manager import EggPluginManager
from extension_point import ExtensionPoint
from import_manager import ImportManager
from service_registry import ServiceRegistry


# Logging.
logger = logging.getLogger(__name__)


class Application(HasTraits):
    """ An extensible, pluggable, application. """

    implements(IApplication)
    
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

    # Fired when a symbol is imported.
    #
    # fixme: We would like to use delegation here, but delegation of events
    # doesn't seem to work in Traits 3.0 8^(
    symbol_imported = Event
    
    #### 'Application' interface ##############################################

    # The extension registry.
    extension_registry = Instance(
        IExtensionRegistry, factory=EggExtensionRegistry
    )

    # The import manager.
    import_manager = Instance(IImportManager, factory=ImportManager)
    
    # The plugin manager (starts and stops plugins etc).
    plugin_manager = Instance(IPluginManager)

    # The service registry.
    service_registry = Instance(IServiceRegistry, factory=ServiceRegistry)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(Application, self).__init__(**traits)

        # This allows the 'ExtensionPoint' trait type to be used as a more
        # convenient way to get the extensions for a given extension point.
        ExtensionPoint.extension_registry = self.extension_registry

        return
    
    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _plugin_manager_default(self):
        """ Initializer. """

        return EggPluginManager(application=self)

    #### Properties ###########################################################

    #### Handlers #############################################################

    def _plugin_manager_changed(self):
        """ Static trait change handler. """

        self.plugin_manager.application = self

        return

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

            # Lifecycle event.
            self.stopped = self._create_application_event()

            logger.debug('---------- application stopped ----------')

        else:
            logger.debug('---------- application stop vetoed ----------')
            
        return not event.veto

    def start_plugin(self, plugin=None, id=None):
        """ Start the specified plugin.

        """

        return self.plugin_manager.start_plugin(plugin, id)

    def stop_plugin(self, plugin=None, id=None):
        """ Stop the specified plugin.

        """

        return self.plugin_manager.stop_plugin(plugin, id)

    def unregister_service(self, service_id):
        """ Unregister a service.

        """

        self.service_registry.unregister_service(service_id)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    @on_trait_change('import_manager.symbol_imported')
    def _when_import_manager_symbol_imported(self, event):
        """ Dynamic trait change handler. """

        self.symbol_imported = event

        return
    
    def _create_application_event(self):
        """ Create an application event. """

        return ApplicationEvent(application=self)
    
#### EOF ######################################################################
