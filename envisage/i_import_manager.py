# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The interface for import managers. """


# Enthought library imports.
from traits.api import Interface


class IImportManager(Interface):
    """ The interface for import managers. """

    def import_symbol(self, symbol_path):
        """ Import the symbol defined by the specified symbol path.

        'symbol_path' is a string containing the path to a symbol through the
        Python package namespace.

        It can be in one of two forms:

        1) 'foo.bar.baz'

           Which is turned into the equivalent of an import statement that
           looks like::

             from foo.bar import baz

           With the value of 'baz' being returned.

        2) 'foo.bar:baz' (i.e. a ':' separating the module from the symbol)

           Which is turned into the equivalent of::

             from foo import bar
             eval('baz', bar.__dict__)

           With the result of the 'eval' being returned.

        The second form is recommended as it allows for nested symbols to be
        retreived, e.g. the symbol path 'foo.bar:baz.bling' becomes::

            from foo import bar
            eval('baz.bling', bar.__dict__)

        The first form is retained for backwards compatability.

        """

#### EOF ######################################################################
