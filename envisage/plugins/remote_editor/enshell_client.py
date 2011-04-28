# Standard library imports
import os

# Local imports
from envisage.plugins import remote_editor
from envisage.plugins.remote_editor.communication.client import Client


class EnshellClient(Client):
    """ A Client that is configured to spawn servers using the config file
        for this application.
    """

    server_prefs = (os.path.join(remote_editor.__path__[0],
                    "preferences.ini"),
                    "enthought.remote_editor")
