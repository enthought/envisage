""" The application interface. """


# Enthought library imports.
from apptools.preferences.api import IPreferences
from traits.api import Event, Instance, Str, VetoableEvent

# Local imports.
from .i_extension_registry import IExtensionRegistry
from .i_import_manager import IImportManager
from .i_plugin_manager import IPluginManager
from .i_service_registry import IServiceRegistry
from .application_event import ApplicationEvent


class IApplication(
        IExtensionRegistry, IImportManager, IPluginManager, IServiceRegistry
    ):
    """ The application interface. """

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

          if application.start():
              application.stop()

        """

#### EOF ######################################################################
