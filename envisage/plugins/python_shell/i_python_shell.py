# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A simple interface for the Python shell. """


# Enthought library imports.
from traits.api import Interface


class IPythonShell(Interface):
    """A simple interface for the Python shell."""

    def bind(self, name, value):
        """Binds a name to a value in the interpreter's namespace."""

    def execute_command(self, command, hidden=True):
        """Execute a command in the interpreter."""

    def execute_file(self, path, hidden=True):
        """Execute a file in the interpreter."""

    def lookup(self, name):
        """Returns the value bound to a name in the interpreter's namespace."""
