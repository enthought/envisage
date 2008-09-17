""" A remote editor plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.plugins.remote_editor.api import IRemoteEditor
from enthought.traits.api import List, Instance, on_trait_change

# Local imports
from envisage_remote_editor import EnvisageRemoteEditorController \
    as RemoteEditorController

class RemoteEditorPlugin(Plugin):
    """ An IPython shell plugin. """

    # Extension point Ids.
    REMOTE_EDITOR   = 'enthought.plugins.remote_editor'
    VIEWS           = 'enthought.envisage.ui.workbench.views'
    ACTION_SETS       = 'enthought.envisage.ui.workbench.action_sets'

    # Our remote controller for the editor
    remote_controller = Instance(RemoteEditorController)

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'enthought.plugins.remote_editor'

    # The plugin's name (suitable for displaying to the user).
    name = 'Remote editor'

    #### Extension points offered by this plugin ##############################

    #### Contributions to extension points made by this plugin ################

    # Our action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """
        from enthought.plugins.remote_editor.plugin.actions import \
            RemoteEditorActionSet
        return [RemoteEditorActionSet]

    ###########################################################################
    # Private interface.
    ###########################################################################

    # Create the central server for spawning shells and editors.
    @on_trait_change('application:started')
    def _create_server(self):
        """ Create the central server for spawning shells and editors and
            register the controller as an envisage service.        
        """
        # Register our client to the server. If the server does not
        # exist, this will create it.
        self.remote_controller = RemoteEditorController(
                    application=self.application)
        self.remote_controller.register()

        self.application.register_service(IRemoteEditor,
                                                self.remote_controller)

        return
 
    @on_trait_change('application:stopping')
    def _unregister_from_server(self):
        """ Unregister this client from the server.
        """
        self.remote_controller.unregister()
        
#### EOF ######################################################################
