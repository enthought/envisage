""" The interface for protocols that handle resource URLs. """


# Enthought library imports.
from enthought.traits.api import Interface


class IResourceProtocol(Interface):
    """ The interface for protocols that handle resource URLs. """

    def file(self, address):
        """ Return a readable file-like object for the specified address.

        Return None if the resource does not exist.

        e.g.::

          protocol.as_file('acme.ui.workbench:colors.ini')

        """

#### EOF ######################################################################
