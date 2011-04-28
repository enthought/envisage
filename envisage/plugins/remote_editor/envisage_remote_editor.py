""" An implementation of a client controlling a remote editor, but also using
    envisage to retrieve an execution engine, and run the commands from the
    editor.
"""

# Standard library imports
import logging

# Enthought library imports
from traits.api import Instance
from envisage.api import Application
from envisage.plugins.python_shell.api import IPythonShell
from pyface.api import GUI

# Local imports
from envisage.plugins.remote_editor.remote_editor_controller import \
    RemoteEditorController

logger = logging.getLogger(__name__)


class EnvisageRemoteEditorController(RemoteEditorController):
    """ An implementation of a client controlling a remote editor, but also
        using envisage to retrieve an execution engine, and run the commands
        from the editor.
    """

    # Tell the Client code to play well with the wx or Qt4 event loop
    ui_dispatch = 'auto'

    # A reference to the Envisage application.
    application = Instance(Application)

    ###########################################################################
    # EnvisageRemoteEditorController interface
    ###########################################################################

    def run_file(self, path):
        """ Called by the server to execute a file.
        """
        shell = self.application.get_service(IPythonShell)
        shell.execute_file(path, hidden=False)

    def run_text(self, text):
        """ Called by the server to execute text.
        """
        shell = self.application.get_service(IPythonShell)
        shell.execute_command(text, hidden=False)

    ###########################################################################
    # Enshell Client interface
    ###########################################################################

    def handle_command(self, command, arguments):
        """ Hande commands coming in from the server.
        """
        if command == "run_file":
            self.run_file(arguments)
            return True
        elif command == "run_text":
            self.run_text(arguments)
            return True
        return False

