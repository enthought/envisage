""" Interface definition for the Remote shell """

# Enthought library imports.
from traits.api import Interface

class IRemoteShell(Interface):
    """ Interface definition for the remote shell """

    def run_file(self, path):
        """ Runs a file in the remote shell.

        """

    def run_text(self, text):
        """ Runs a string in the remote shell.

        """

#### EOF ######################################################################

