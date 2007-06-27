""" The interface for import managers. """


# Enthought library imports.
from enthought.traits.api import Event, Interface


class IImportManager(Interface):
    """ The interface for import managers. """

    # Fired when a symbol is imported.
    symbol_imported = Event

    def import_symbol(self, symbol_path):
        """ Import the symbol defined by the specified symbol path.

        'symbol_path' is a string containing the path to a symbol through the
        Python package namespace.

        It can be in one of two forms:-

        1) 'foo.bar.baz'

        Which is turned into the equivalent of an import statement that looks
        like:-

        from foo.bar import baz

        With the value of 'baz' being returned.
        
        2) 'foo.bar:baz.bling'

        Which is turned into the equivalent of:-

        from foo import bar
        eval('baz.bling', bar.__dict__)

        With the result of the 'eval' being returned.
        
        """

#### EOF ######################################################################
