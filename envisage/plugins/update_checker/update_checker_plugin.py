
# Enthought library imports
from envisage.api import Plugin
from traits.api import Bool, Callable, Event, Int, Instance, Str, Trait

# Local, relative imports
from .update_info import UpdateInfo


# The globally unique ID of this plugin
ID = "envisage.plugins.update_checker"


class UpdateCheckerPlugin(Plugin):

    name = "Update Checker Plugin"

    # The URI to an updates.xml file.  Although this can be a local path,
    # typically it will be a URL.
    location = Str("localhost")

    # Update

    # Should the plugin automatically check for updates?
    check_automatically = Bool(True)

    # The frequency with which to check for updates
    # Can be "startup", which means at application startup, or an integer number
    # of seconds
    # TODO: Contribute a preference for this!
    check_frequency = Trait("startup", "startup", Int)

    # Whether or not to display a dialog informing the user of available
    # updates
    display_dialog = Bool(True)

    # The UpdateInfo object that contains the actual update information.
    # Regardless of whether or not a dialog is displayed to the user, this
    # attribute will be populated with the appropriate information.
    update_info = Instance(UpdateInfo)

    # This event fires every time the UpdateCheckerPlugin is invoked and
    # determines that an application update is available.
    update_needed = Event()  #Event(ApplicationEvent)

    #========================================================================
    # Plugin interface
    #========================================================================

    def start(self):
        """ Make the appropriate contributions
        """

        self.application.on_trait_change("started", self._check_for_update)

    def stop(self):
        """ Clean up
        """

        self.application.on_trait_change("started", self._check_for_update, remove=True)

    #========================================================================
    # Public methods
    #========================================================================

    def _check_for_update(self):
        pass


