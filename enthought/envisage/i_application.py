""" The application interface. """


# Enthought library imports.
from enthought.preferences.api import IPreferences
from enthought.traits.api import Event, Instance, Str, VetoableEvent

# Local imports.
from i_extension_registry import IExtensionRegistry
from i_import_manager import IImportManager
from i_plugin_manager import IPluginManager
from i_service_registry import IServiceRegistry
from application_event import ApplicationEvent


class IApplication(
        IExtensionRegistry, IImportManager, IPluginManager, IServiceRegistry
    ):
    """ The application interface. """

    # A directory that the application can read and write to at will.
    home = Str

    # The application's globally unique identifier.
    id = Str

    # The root preferences node.
    preferences = Instance(IPreferences)

    #### Events ####
    
    # Fired when the application is starting. This is the first thing that
    # happens when the 'start' method is called.
    starting = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been started.
    started = Event(ApplicationEvent)

    # Fired when the plugin manager is stopping. This is the first thing that
    # happens when the 'stop' method is called.
    stopping = VetoableEvent(ApplicationEvent)

    # Fired when all plugins have been stopped.
    stopped = Event(ApplicationEvent)

    def run(self):
        """ Run the application.

        The same as::

          application.start()
          application.stop()

        """

#### EOF ######################################################################
