"""
An implementation of a client controlling a remote editor, but also using
envisage to retrieve an execution engine, and run the commands from the
editor.
"""

# Standard library imports
import logging

# Enthought library imports
from enthought.traits.api import Instance
from enthought.envisage.api import Application
from enthought.plugins.python_shell.api import IPythonShell
from enthought.pyface.api import GUI

# Local imports
from enthought.plugins.remote_editor.remote_editor_controller import \
    RemoteEditorController

logger = logging.getLogger(__name__)

class EnvisageRemoteEditorController(RemoteEditorController):
    """ An implementation of a client controlling a remote editor, but also 
        using envisage to retrieve an execution engine, and run the commands 
        from the editor.
    """

    # Tell the client code to play well with the wx event loop
    wx = True

    # A reference to the Envisage application.
    application = Instance(Application)

    ###########################################################################
    # EnvisageRemoteEditorController interface
    ###########################################################################
    def run_file(self, path):
        """ Called by the server to execute a file.
        """
        shell = self.application.get_service(IPythonShell)
        shell.execute_command('%run ' + '"%s"' % path, hidden=False)


    def run_text(self, text):
        """ Called by the server to execute text.
        """
        shell = self.application.get_service(IPythonShell)
        shell.execute_command(text, hidden=False)


    ###########################################################################
    # Enshell Client interface
    ###########################################################################
    def handle_command(self, command, arguments):
        GUI.invoke_later(self._handle_command, command, arguments)

    def _handle_command(self, command, arguments):
        """ Hande commands coming in from the server.
        """
        logger.info('Enshell client recieved message: %s %s' 
                            % (command, arguments))
        if command == "run_file":
            self.run_file(arguments)
            return True
        elif command == "run_text":
            self.run_text(arguments)
            return True
        return False


    def send_command(self, command, *args):
        """ Sends commands to the remote server.
        """
        logger.info('Enshell client sending command: %s, %s' %
                        (command, args))
        RemoteEditorController.send_command(self, command, *args)

