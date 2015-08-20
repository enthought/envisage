"""
A client controlling a remote editor.
"""

# Enthought library imports
from traits.api import provides

# Local imports
from envisage.plugins.remote_editor.communication.client import Client
from .i_remote_editor import IRemoteEditor


@provides(IRemoteEditor)
class RemoteEditorController(Client):
    """ A Client used to control a remote editor.
    """
    # Client interface

    self_type = "python_shell"
    other_type = "python_editor"

    def new_file(self):
        self.send_command('new')

    def open_file(self, filename):
        self.send_command('open', filename)


