# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The default import manager implementation. """


# Enthought library imports.
from traits.api import HasTraits, provides

# Local imports.
from .i_import_manager import IImportManager


@provides(IImportManager)
class ImportManager(HasTraits):
    """ The default import manager implementation.

    Its just a guess, but I think using an import manager to do all imports
    will make debugging easier (as opposed to just letting imports happen from
    all over the place).

    """

    ###########################################################################
    # 'IImportManager' interface.
    ###########################################################################

    def import_symbol(self, symbol_path):
        """ Import the symbol defined by the specified symbol path. """

        if ':' in symbol_path:
            module_name, symbol_name = symbol_path.split(':')

            module = self._import_module(module_name)
            symbol = eval(symbol_name, module.__dict__)

        else:
            components = symbol_path.split('.')

            module_name = '.'.join(components[:-1])
            symbol_name = components[-1]

            module = __import__(
                module_name, globals(), locals(), [symbol_name]
            )

            symbol = getattr(module, symbol_name)

        # Event notification.
        self.symbol_imported = symbol

        return symbol

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _import_module(self, module_name):
        """ Import the module with the specified (and possibly dotted) name.

        Returns the imported module.

        This method is copied from the documentation of the '__import__'
        function in the Python Library Reference Manual.

        """

        module = __import__(module_name)

        components = module_name.split('.')
        for component in components[1:]:
            module = getattr(module, component)

        return module

#### EOF ######################################################################
