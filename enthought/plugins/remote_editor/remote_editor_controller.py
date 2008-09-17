"""
A client controlling a remote editor.
"""

# Standard library imports
import os

# Enthought library imports
from enthought.traits.api import implements

# Local imports
import enthought.plugins.remote_editor as remote_editor
from enthought.plugins.remote_editor.communication.client import Client
from i_remote_editor import IRemoteEditor


class RemoteEditorController(Client):
    """ A Client used to control a remote editor.
    """
    implements(IRemoteEditor)

    # Client interface

    self_type = "python_shell"
    other_type = "python_editor"

    # The server preferences. Used while spawning the server, to give it
    # the different clients it can spawn.
    server_prefs = (os.path.join(remote_editor.__path__[0], 
                    "preferences.ini"),
                    "enshell.applications")   

    def new_file(self):
        self.send_command('new')

    def open_file(self, filename):
        self.send_command('open', filename)


