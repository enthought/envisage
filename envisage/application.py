# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An extensible, pluggable, application. """


# Standard library imports.
import logging, os

# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from apptools.preferences.api import IPreferences, ScopedPreferences
from apptools.preferences.api import set_default_preferences
from traits.api import Delegate, Event, HasTraits, Instance, Str
from traits.api import VetoableEvent, provides

# Local imports.
from .i_application import IApplication
from .i_extension_registry import IExtensionRegistry
from .i_import_manager import IImportManager
from .i_plugin_manager import IPluginManager
from .i_service_registry import IServiceRegistry

from .application_event import ApplicationEvent
from .import_manager import ImportManager


# Logging.
logger = logging.getLogger(__name__)


@provides(IApplication)
class Application(HasTraits):
    """ An extensible, pluggable, application.

    This class handles the common case for non-GUI applications, and it is
    intended to be subclassed to change start/stop behaviour etc.

    """

    #### 'IApplication' interface #############################################

    # The application's globally unique identifier.
    id = Str

    # The name of a directory (created for you) to which the application can
    # read and write non-user accessible data, i.e. configuration information,
    # preferences, etc.
    home = Str

    # The name of a directory (created for you upon access) to which the
    # application can read and write user-accessible data, e.g. projects created
    # by the user.
    user_data = Str

    # The root preferences node.
    preferences = Instance(IPreferences)

    #### Events ####

    # Fired when the application is starting.
    starting = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been started.
    started = Event(ApplicationEvent)

    # Fired when the application is stopping.
    stopping = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been stopped.
    stopped = Event(ApplicationEvent)

    #### 'IPluginManager' interface ###########################################

    #### Events ####

    # Fired when a plugin has been added.
    plugin_added = Delegate('plugin_manager', modify=True)

    # Fired when a plugin has been removed.
    plugin_removed = Delegate('plugin_manager', modify=True)

    #### 'Application' interface ##############################################

    # These traits allow application developers to build completely different
    # styles of extensible application. It allows Envisage to be used as a
    # framework for frameworks ;^)
    #
    # The extension registry.
    extension_registry = Instance(IExtensionRegistry)

    # The plugin manager (starts and stops plugins etc).
    plugin_manager = Instance(IPluginManager)

    # The service registry.
    service_registry = Instance(IServiceRegistry)

    #### Private interface ####################################################

    # The import manager.
    _import_manager = Instance(IImportManager, factory=ImportManager)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, plugins=None, **traits):
        """ Constructor.

        We allow the caller to specify an initial list of plugins, but the list
        itself is not part of the public API. To add and remove plugins after
        after construction, use the 'add_plugin' and 'remove_plugin' methods
        respectively. The application is also iterable, so to iterate over the
        plugins use 'for plugin in application: ...'.

        """

        super(Application, self).__init__(**traits)

        # fixme: We have to initialize the application home here (i.e. we can't
        # wait until the 'home' trait is accessed) because the scoped
        # preferences uses 'ETSConfig.application' home as the name of the
        # default preferences file.
        self._initialize_application_home()

        # Set the default preferences node used by the preferences package.
        # This allows 'PreferencesHelper' and 'PreferenceBinding' instances to
        # be used as more convenient ways to access preferences.
        #
        # fixme: This is another sneaky global!
        set_default_preferences(self.preferences)

        # We allow the caller to specify an initial list of plugins, but the
        # list itself is not part of the public API. To add and remove plugins
        # after construction, use the 'add_plugin' and 'remove_plugin' methods
        # respectively. The application is also iterable, so to iterate over
        # the plugins use 'for plugin in application: ...'.
        if plugins is not None:
            for plugin in plugins:
                self.add_plugin(plugin)

        return

    ###########################################################################
    # 'IApplication' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _home_default(self):
        """ Trait initializer. """

        return ETSConfig.application_home

    def _user_data_default(self):
        """ Trait initializer. """

        user_data = os.path.join(
            ETSConfig.user_data, self.id
        )

        # Make sure it exists!
        if not os.path.exists(user_data):
            os.makedirs(user_data)

        return user_data

    def _preferences_default(self):
        """ Trait initializer. """

        return ScopedPreferences()

    #### Methods ##############################################################

    def run(self):
        """ Run the application. """

        if self.start():
            self.stop()

        return

    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def add_extension_point_listener(self, listener, extension_point_id=None):
        """ Add a listener for extensions being added/removed. """

        self.extension_registry.add_extension_point_listener(
            listener, extension_point_id
        )

        return

    def add_extension_point(self, extension_point):
        """ Add an extension point. """

        self.extension_registry.add_extension_point(extension_point)

        return

    def get_extensions(self, extension_point_id):
        """ Return a list containing all contributions to an extension point.

        """

        return self.extension_registry.get_extensions(extension_point_id)

    def get_extension_point(self, extension_point_id):
        """ Return the extension point with the specified Id. """

        return self.extension_registry.get_extension_point(extension_point_id)

    def get_extension_points(self):
        """ Return all extension points that have been added to the registry.

        """

        return self.extension_registry.get_extension_points()

    def remove_extension_point_listener(self,listener,extension_point_id=None):
        """ Remove a listener for extensions being added/removed. """

        self.extension_registry.remove_extension_point_listener(
            listener, extension_point_id
        )

        return

    def remove_extension_point(self, extension_point_id):
        """ Remove an extension point. """

        self.extension_registry.remove_extension_point(extension_point_id)

        return

    def set_extensions(self, extension_point_id, extensions):
        """ Set the extensions contributed to an extension point. """

        self.extension_registry.set_extensions(extension_point_id, extensions)

        return

    ###########################################################################
    # 'IImportManager' interface.
    ###########################################################################

    def import_symbol(self, symbol_path):
        """ Import the symbol defined by the specified symbol path. """

        return self._import_manager.import_symbol(symbol_path)

    ###########################################################################
    # 'IPluginManager' interface.
    ###########################################################################

    def __iter__(self):
        """ Return an iterator over the manager's plugins. """

        return iter(self.plugin_manager)

    def add_plugin(self, plugin):
        """ Add a plugin to the manager. """

        self.plugin_manager.add_plugin(plugin)

        return

    def get_plugin(self, plugin_id):
        """ Return the plugin with the specified Id. """

        return self.plugin_manager.get_plugin(plugin_id)

    def remove_plugin(self, plugin):
        """ Remove a plugin from the manager. """

        self.plugin_manager.remove_plugin(plugin)

        return

    def start(self):
        """ Start the plugin manager.

        Returns True unless the start was vetoed.

        """

        # fixme: This method is notionally on the 'IPluginManager' interface
        # but that interface knows nothing about the vetoable events etc and
        # hence doesn't have a return value.
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

    def start_plugin(self, plugin=None, plugin_id=None):
        """ Start the specified plugin. """

        return self.plugin_manager.start_plugin(plugin, plugin_id)

    def stop(self):
        """ Stop the plugin manager.

        Returns True unless the stop was vetoed.

        """

        # fixme: This method is notionally on the 'IPluginManager' interface
        # but that interface knows nothing about the vetoable events etc and
        # hence doesn't have a return value.
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

    def stop_plugin(self, plugin=None, plugin_id=None):
        """ Stop the specified plugin. """

        return self.plugin_manager.stop_plugin(plugin, plugin_id)

    ###########################################################################
    # 'IServiceRegistry' interface.
    ###########################################################################

    def get_required_service(self, protocol, query='', minimize='',maximize=''):
        """ Return the service that matches the specified query.

        Raise a 'NoSuchServiceError' exception if no such service exists.

        """

        service = self.service_registry.get_required_service(
            protocol, query, minimize, maximize
        )

        return service

    def get_service(self, protocol, query='', minimize='', maximize=''):
        """ Return at most one service that matches the specified query. """

        service = self.service_registry.get_service(
            protocol, query, minimize, maximize
        )

        return service

    def get_service_from_id(self, service_id):
        """ Return the service with the specified id. """

        return self.service_registry.get_service_from_id(service_id)

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service. """

        return self.service_registry.get_service_properties(service_id)

    def get_services(self, protocol, query='', minimize='', maximize=''):
        """ Return all services that match the specified query. """

        services = self.service_registry.get_services(
            protocol, query, minimize, maximize
        )

        return services

    def register_service(self, protocol, obj, properties=None):
        """ Register a service. """

        service_id = self.service_registry.register_service(
            protocol, obj, properties
        )

        return service_id

    def set_service_properties(self, service_id, properties):
        """ Set the dictionary of properties associated with a service. """

        self.service_registry.set_service_properties(service_id, properties)

        return

    def unregister_service(self, service_id):
        """ Unregister a service. """

        self.service_registry.unregister_service(service_id)

        return

    ###########################################################################
    # 'Application' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _extension_registry_default(self):
        """ Trait initializer. """

        # Do the import here to emphasize the fact that this is just the
        # default implementation and that the application developer is free
        # to override it!
        from .plugin_extension_registry import PluginExtensionRegistry

        return PluginExtensionRegistry(plugin_manager=self)

    def _plugin_manager_default(self):
        """ Trait initializer. """

        # Do the import here to emphasize the fact that this is just the
        # default implementation and that the application developer is free
        # to override it!
        from .plugin_manager import PluginManager

        return PluginManager(application=self)

    def _service_registry_default(self):
        """ Trait initializer. """

        # Do the import here to emphasize the fact that this is just the
        # default implementation and that the application developer is free
        # to override it!
        from .service_registry import ServiceRegistry

        return ServiceRegistry()

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    # fixme: We have this to make it easier to assign a new plugin manager
    # at construction time due to the fact that the plugin manager needs a
    # reference to the application and vice-versa, e.g. we can do
    #
    #    application = Application(plugin_manager=EggPluginManager())
    #
    # If we didn't have this then we would have to do this:-
    #
    #    application = Application()
    #    application.plugin_manager = EggPluginManager(application=application)
    #
    # Of course, it would be better if the plugin manager didn't require a
    # reference to the application at all (it currently uses it to set the
    # 'application' trait of plugin instances - but that is only done for the
    # same reason as this (i.e. it is nice to be able to pass plugins into the
    # application constructor).
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

#### EOF ######################################################################
