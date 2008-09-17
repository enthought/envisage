# Standard library imports
import os

# Local imports
from enthought.plugins import remote_editor
from enthought.plugins.remote_editor.communication.client import Client


class EnshellClient(Client):
    """ A Client that is configured to spawn servers using the config file
        for this application.
    """

    server_prefs = (os.path.join(remote_editor.__path__[0], 
                    "preferences.ini"),
                    "enshell.applications")
