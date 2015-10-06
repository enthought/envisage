""" Classes used to represent classes. """


# Standard library imports.
import ast

# Enthought library imports.
from traits.api import Any, Dict, HasTraits, Instance, Int, List
from traits.api import Str

# Local imports.
from .assign import AssignFactory
from .function import FunctionFactory
from .namespace import Namespace
from ..._compat import STRING_BASE_CLASS


class Klass(Namespace):
    """ A class. """

    #### 'Klass' interface ####################################################

    # The namespace that the class is defined in (this is *usually* a module,
    # but of course classes can be defined anywhere in Python).
    namespace = Instance(Namespace)

    # The line number in the module at which the class appears.
    lineno = Int

    # The name of the class.
    name = Str

    # The class' doc-string (None if there is no doc string, a string if there
    # is).
    doc = Any

    # The class' base classes.
    bases = List(Str)

    # The class' attributes.
    attributes = Dict

    # The class' traits.
    traits = Dict

    # The class' methods.
    methods = Dict

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Returns an informal string representation of the object. """

        return 'Klass %s at %d' % (self.name, self.lineno)

    def __getstate__(self):
        """ Returns the state of the object for pickling. """

        state = {}
        state['namespace'] = self.namespace
        state['lineno'] = self.lineno
        state['name'] = self.name
        state['doc'] = self.doc
        state['bases'] = self.bases
        state['attributes'] = self.attributes
        state['traits'] = self.traits
        state['methods'] = self.methods

        return state

    def __setstate__(self, state):
        """ Sets the state object duting unpickling. """

        self.namespace = state['namespace']
        self.lineno = state['lineno']
        self.name = state['name']
        self.doc = state['doc']
        self.bases = state['bases']
        self.attributes = state['attributes']
        self.traits = state['traits']
        self.methods = state['methods']

        return


class KlassFactory(HasTraits):
    """ A factory for classes. """

    ###########################################################################
    # 'KlassFactory' interface.
    ###########################################################################

    def from_ast(self, namespace, node):
        """ Creates a class from an AST node. """

        # Create a new class.
        klass = Klass(
            namespace = namespace,
            lineno    = node.lineno,
            name      = node.name,
            doc       = ast.get_docstring(node, clean=False),
            bases     = [self._get_name(base) for base in node.bases]
        )

        # Walk the AST picking out the things we care about!
        KlassVisitor(klass).visit(node)

        return klass

    ###########################################################################
    # Private interface.
    ###########################################################################

    # fixme: This same method is used in 'AssignVisitor'.
    def _get_name(self, node):
        """ Returns the (possibly dotted) name from a node. """

        if isinstance(node, STRING_BASE_CLASS):
            name = node
        elif isinstance(node, ast.Name):
            name = node.id
        else:
            names = [self._get_name(child) for child in ast.walk(node) if child is not node]
            name = '.'.join(names)

        return name


class KlassVisitor(ast.NodeVisitor):
    """ An AST visitor for classes. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, klass):
        """ Creates a new visitor. """

        self.klass = klass

        # Factories used to create klasses, functions and assignments from
        # AST nodes.
        self._function_factory = FunctionFactory()
        self._assign_factory   = AssignFactory()

        return

    ###########################################################################
    # 'ASTVisitor' interface.
    ###########################################################################

    def visit_FunctionDef(self, node):
        """ Visits a function node. """

        function = self._function_factory.from_ast(self.klass, node)

        self.klass.locals[node.name] = function
        self.klass.methods[node.name] = function

        return

    def visit_Assign(self, node):
        """ Visits an assignment node. """

        assign = self._assign_factory.from_ast(self.klass, node)

        # Does the assigment look like it *might* be a trait? (i.e., it is NOT
        # an expression or a constant etc.).
        if assign.source:
            assign.is_trait = self.klass.is_trait(assign.source)

        else:
            assign.is_trait = False

        for target in assign.targets:
            self.klass.locals[target] = assign
            self.klass._is_trait[target] = assign.is_trait

            if assign.is_trait:
                self.klass.traits[target] = assign

            else:
                self.klass.attributes[target] = assign

        return

#### EOF ######################################################################
