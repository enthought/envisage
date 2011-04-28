""" A simple interface for the Python shell. """


# Enthought library imports.
from traits.api import Interface


class IPythonShell(Interface):
    """ A simple interface for the Python shell. """

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace.

        """

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter.

        """

    def execute_file(self, path, hidden=True):
        """ Execute a file in the interpreter.

        """

    def lookup(self, name):
        """ Returns the value bound to a name in the interpreter's namespace.

        """

#### EOF ######################################################################
