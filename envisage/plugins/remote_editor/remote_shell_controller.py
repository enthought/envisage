"""
A client controlling a remote shell.
"""

# Enthought library imports
from traits.api import provides

# Local imports
from envisage.plugins.remote_editor.communication.client import Client
from .i_remote_shell import IRemoteShell


@provides(IRemoteShell)
class RemoteShellController(Client):
    """ A Client used to control a remote shell.
    """
    #------------------------------------------------------
    # Client interface
    #------------------------------------------------------

    self_type = "python_editor"
    other_type = "python_shell"

    #------------------------------------------------------
    # RemoteShell interface
    #------------------------------------------------------

    def run_file(self, path):
        self.send_command('run_file', path)

    def run_text(self, text):
        self.send_command('run_text', text)
