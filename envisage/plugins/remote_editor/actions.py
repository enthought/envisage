from envisage.ui.action.api import Action, ActionSet, Group
from pyface.api import FileDialog, OK
from pyface.action.api import Action as PyfaceAction
from envisage.plugins.remote_editor.api import IRemoteEditor



def get_server(window):
    """ Given an application window, retrieve the communication server.
    """
    return window.application.get_service(IRemoteEditor)

################################################################################
# Groups
################################################################################
file_group = Group(
    id='RemoteEditorFileGroup',
    path='MenuBar/File',
    before='ExitGroup'
)


################################################################################
# `OpenScript` class.
################################################################################
class OpenScript(PyfaceAction):
    """ An action that opens a Python file in a remote editor. """

    tooltip      = "Open a Python script in separate editor."

    description  = "Open a Python script in separate editor."


    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        server = get_server(self.window)

        wildcard = 'Python files (*.py)|*.py'

        parent = self.window.control
        dialog = FileDialog(parent=parent,
                            title='Open Python script in separate editor',
                            action='open', wildcard=wildcard
                            )
        if dialog.open() == OK:
            server.open_file(dialog.path)


open_script = Action(
    path        = "MenuBar/File",
    class_name  = __name__ + '.OpenScript',
    name        = "Open script in editor",
    group       = "RemoteEditorFileGroup",
)

################################################################################
# `NewScript` class.
################################################################################
class NewScript(PyfaceAction):
    """ An action that opens a new file in a remote editor. """

    tooltip       = "Open a new file in separate editor."

    description   = "Open a new file in separate editor."

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        server = get_server(self.window)
        server.new_file()


new_script = Action(
    path        = "MenuBar/File",
    class_name  = __name__ + '.NewScript',
    name        = "New script in editor",
    group       = "RemoteEditorFileGroup",
)


################################################################################
# `RemoteEditorActionSet` class.
################################################################################
class RemoteEditorActionSet(ActionSet):
    """ The default action set for the remote editor plugin. """

    groups = [file_group, ]

    actions = [open_script, new_script]
