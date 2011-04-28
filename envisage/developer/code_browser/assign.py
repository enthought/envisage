""" Classes used to represent assignment statements. """


# Standard library imports.
import compiler
from compiler.visitor import ASTVisitor

# Enthought library imports.
from traits.api import Any, Bool, HasTraits, Instance, Int, List, Str


class Assign(HasTraits):
    """ An assignment statement. """

    #### 'Assign' interface ###################################################

    # The namespace that the assignment statement is in.
    namespace = Instance(
        'envisage.developer.code_browser.namespace.Namespace'
    )

    # The line number within the module at which the assignment statement
    # appears.
    lineno = Int

    # The names being assigned to (in Python there can be more than one).
    targets = List(Str)

    # The expression being assigned to the targets (an AST node).
    expr = Any

    # We only care about assignments to trait types, not literals or
    # expressions etc.
    source = Str

    # Is this a trait assignment?
    is_trait = Bool(False)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Returns an informal string representation of the object. """

        return 'Assign %s at %d' % (', '.join(self.targets), self.lineno)


class AssignFactory(HasTraits):
    """ A factory for assignment statements. """

    ###########################################################################
    # 'AssignFactory' interface.
    ###########################################################################

    def from_ast(self, namespace, node):
        """ Creates an assignment statement from an AST node. """

        # Create a new assignment statement.
        assign = Assign(
            namespace = namespace,
            lineno    = node.lineno,
            expr      = node.expr
        )

        # Walk the AST picking out the things we care about!
        compiler.walk(node, AssignVisitor(assign))

        return assign


class AssignVisitor(ASTVisitor):
    """ An AST visitor for assigment statements. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, assign):
        """ Creates a new visitor. """

        self.assign = assign

        return

    ###########################################################################
    # 'ASTVisitor' interface.
    ###########################################################################

    def visitAssName(self, node):
        """ Visits an assignment node. """

        self.assign.targets.append(node.name)

        return

    def visitCallFunc(self, node):
        """ Visits a function call node. """

        function_name = self._get_name(node.node)
        self.assign.source = function_name

        return

    def visitName(self, node):
        """ Visits a name node. """

        self.assign.source = node.name

        return

    def visitGetattr(self, node):
        """ Visits a getattr node. """

        self.assign.source = self._get_name(node)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_name(self, node):
        """ Returns the (possibly dotted) name from a node. """

        # fixme: Work out when node can be none here!!!!! I think it is safe
        # to ignore it in terms of working out what is a trait, but it would
        # be nice to know what is going on ;^)
        if node is not None:
            if isinstance(node, basestring):
                name = node

            elif not hasattr(node, 'getType'):
                name = ''

            elif node.getType() == compiler.ast.Name:
                name = node.name

            else:
                names = [self._get_name(child) for child in node.getChildren()]
                name = '.'.join(names)

        else:
            name = ''

        return name

#### EOF ######################################################################



