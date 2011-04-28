""" The interface for protocols that handle resource URLs. """


# Enthought library imports.
from traits.api import Interface


class IResourceProtocol(Interface):
    """ The interface for protocols that handle resource URLs. """

    def file(self, address):
        """ Return a readable file-like object for the specified address.

        Raise a 'NoSuchResourceError' if the resource does not exist.

        e.g.::

          protocol.file('acme.ui.workbench/preferences.ini')

        """

#### EOF ######################################################################
