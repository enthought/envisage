""" Classes used to represent functions and methods. """

# Standard library imports.
import ast

# Enthought library imports.
from traits.api import Any, HasTraits, Instance, Int, Str

# Local imports.
from .namespace import Namespace


class Function(Namespace):
    """ A function. """

    #### 'Function' interface #################################################

    # The namespace that the function is defined in.
    namespace = Instance(Namespace)

    # The line number in the module at which the function appears.
    lineno = Int

    # The name of the function.
    name = Str

    # The function's doc-string (None if there is no doc string, a string if
    # there is).
    doc = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Returns an informal string representation of the object. """

        return 'Function %s at %d' % (self.name, self.lineno)


class FunctionFactory(HasTraits):
    """ A factory for classes. """

    ###########################################################################
    # 'FunctionFactory' interface.
    ###########################################################################

    def from_ast(self, namespace, node):
        """ Creates a class from an AST node. """

        # Create a new function.
        function = Function(
            namespace = namespace,
            lineno    = node.lineno,
            name      = node.name,
            doc       = ast.get_docstring(node, clean=False)
        )

        return function

#### EOF ######################################################################



