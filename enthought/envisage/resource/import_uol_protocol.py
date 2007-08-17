""" A UOL protocol that imports a symbol. """


# Local imports.
from uol_protocol import UOLProtocol


class ImportUOLProtocol(UOLProtocol):
    """ A UOL protocol that imports a symbol. """

    def lookup(self, application, address):
        """ Resolve an address to produce an object. """

        return application.import_symbol(address)

#### EOF ######################################################################
