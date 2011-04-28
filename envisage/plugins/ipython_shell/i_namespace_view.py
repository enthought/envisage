""" Interface definition for the Namespace view """

# Enthought library imports.
from traits.api import Interface

class INamespaceView(Interface):
    """ Interface definition for the Namespace view """

    def _on_names_changed(self, new):
        """ Handler to track the changes in the namespace viewed.

        """

#### EOF ######################################################################
