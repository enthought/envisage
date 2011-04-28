""" Interface definition for the Remote editor """

# Enthought library imports.
from traits.api import Interface

class IRemoteEditor(Interface):
    """ Interface definition for the Namespace view """

    def new_file(self):
        """ Creates a new file in the remote editor.

        """

    def open_file(self, filename):
        """ Opens a file in the remote editor.

        """

#### EOF ######################################################################

