""" A plugin for controlling a remote editor. """

# Enthought library imports.
from envisage.api import Plugin
from envisage.plugins.remote_editor.api import IRemoteEditor
from traits.api import List, Instance, Any, on_trait_change

# Local imports
from .envisage_remote_editor import EnvisageRemoteEditorController \
    as RemoteEditorController

ID = 'envisage.plugins.remote_editor'


class RemoteEditorPlugin(Plugin):
    """ A plugin for controlling a remote editor. """

    # Extension point Ids.
    REMOTE_EDITOR     = ID
    ACTION_SETS       = 'envisage.ui.workbench.action_sets'
    PREFERENCES       = 'envisage.preferences'
    PREFERENCES_PAGES = 'envisage.ui.workbench.preferences_pages'

    # Our remote controller for the editor
    remote_controller = Instance(RemoteEditorController)

    # The shell and editor commands
    server_prefs = Any

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.plugins.remote_editor'

    # The plugin's name (suitable for displaying to the user).
    name = 'Remote editor'

    #### Extension points offered by this plugin ##############################

    #### Contributions to extension points made by this plugin ################

    # Our action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    # Preferences pages.
    # FIXME: Create a UI for remote editor preferences
    #preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    # Preferences.
    preferences = List(contributes_to=PREFERENCES)

    def _action_sets_default(self):
        """ Trait initializer. """
        from envisage.plugins.remote_editor.actions import \
            RemoteEditorActionSet
        return [ RemoteEditorActionSet ]

    def _preferences_default(self):
        """ Trait initializer. """
        return [ 'pkgfile://%s/preferences.ini' % ID ]

    def _preferences_pages_default(self):
        """ Trait initializer. """
        from envisage.plugins.remote_editor.preference_pages \
            import RemoteEditorPreferencesPage
        return [ RemoteEditorPreferencesPage ]

    ###########################################################################
    # Private interface.
    ###########################################################################

    # Create the central server for spawning shells and editors.
    @on_trait_change('application:started')
    def _create_server(self):
        """ Create the central server for spawning shells and editors and
            register the controller as an envisage service.
        """
        # Register our client to the server. If the server does not exist, this
        # will create it.
        self.remote_controller = RemoteEditorController(
            application=self.application)

        # XXX I don't like this at all
        if self.server_prefs:
            self.remote_controller.server_prefs = self.server_prefs

        self.remote_controller.register()

        self.application.register_service(IRemoteEditor, self.remote_controller)

    @on_trait_change('application:stopping')
    def _unregister_from_server(self):
        """ Unregister this client from the server.
        """
        self.remote_controller.unregister()

#### EOF ######################################################################
