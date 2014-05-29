""" Classes used to represent modules. """


# Standard library imports.
import ast, os

# Enthought library imports.
from apptools.io.api import File
from traits.api import Any, Dict, HasTraits, Instance, Str

# Local imports.
from .assign import Assign, AssignFactory
from .function import Function, FunctionFactory
from .klass import Klass, KlassFactory
from .namespace import Namespace


class Module(Namespace):
    """ A module. """

    #### 'Module' interface ###################################################

    # The namespace that the module is defined in. If the module is in a
    # package then this will be the appropriate 'Package' instance, otherwise
    # it will be None.
    namespace = Instance(Namespace)

    # The absolute filename of the module.
    filename = Str

    # The name of the module (this is currently the fully qualified name i.e.,
    # it includes the names of the packages that the module is contained in).
    name = Str

    # The module's doc-string (None if there is no doc string, a string if
    # there is).
    doc = Any

    # The module-level attributes.
    attributes = Dict

    # The classes defined in the module.
    klasses = Dict

    # The module-level functions.
    functions = Dict

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Returns an informal string representation of the object. """

        return 'Module %s' % self.filename

    def __getstate__(self):
        """ Returns the state of the object for pickling. """

        state = {}
        state['namespace'] = self.namespace
        state['filename'] = self.filename
        state['name'] = self.name
        state['doc'] = self.doc
        state['attributes'] = self.attributes
        state['klasses'] = self.klasses
        state['functions'] = self.functions

        return state

    def __setstate__(self, state):
        """ Sets the state object duting unpickling. """

        self.namespace = state['namespace']
        self.filename = state['filename']
        self.name = state['name']
        self.doc = state['doc']
        self.attributes = state['attributes']
        self.klasses = state['klasses']
        self.functions = state['functions']

        return


class ModuleFactory(HasTraits):
    """ A factory for modules. """

    ###########################################################################
    # 'ModuleFactory' interface.
    ###########################################################################

    def from_file(self, filename, namespace=None):
        """ Creates a module by parsing a file. """

        # Parse the file.
        with open(filename) as f:
            node = ast.parse(f.read())

        # Create a new module.
        module = Module(
            namespace = namespace,
            filename  = filename,
            name      = self._get_module_name(filename),
            doc       = ast.get_docstring(node, clean=False),
        )

        # Walk the AST picking out the things we care about!
        ModuleVisitor(module).visit(node)

        return module

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_module_name(self, filename):
        """ Get the fully qualified module name for a filename.

        e.g. if the filename is:-

        '/enthought/envisage/core/core_plugin_definition.py'

        we would return:-

        'envisage.core.core_plugin_definition'

        """

        # Get the name of the module minus the '.py'
        module, ext = os.path.splitext(os.path.basename(filename))

        # Start with the actual module name.
        module_path = [module]

        # If the directory is a Python package then add it to the module path.
        parent = File(os.path.dirname(filename))
        while parent.is_package:
            module_path.insert(0, parent.name)
            parent = parent.parent

        return '.'.join(module_path)


class ModuleVisitor(ast.NodeVisitor):
    """ An AST visitor for top-level modules. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, module):
        """ Creates a new visitor. """

        self.module = module

        # Factories used to create klasses, functions and assignments from
        # AST nodes.
        self._klass_factory    = KlassFactory()
        self._function_factory = FunctionFactory()
        self._assign_factory   = AssignFactory()

        return

    ###########################################################################
    # 'NodeVisitor' interface.
    ###########################################################################

    def visit_ClassDef(self, node):
        """ Visits a class node. """
        klass = self._klass_factory.from_ast(self.module, node)

        self.module.locals[node.name] = klass
        self.module.klasses[node.name] = klass

        return

    def visit_FunctionDef(self, node):
        """ Visits a function node. """

        function = self._function_factory.from_ast(self.module, node)

        self.module.locals[node.name] = function
        self.module.functions[node.name] = function

        return

    def visit_Assign(self, node):
        """ Visits an assignment node. """

        assign = self._assign_factory.from_ast(self.module, node)

        # Does the assigment look like it *might* be a trait? (i.e., it is NOT
        # an expression or a constant etc.).
        if len(assign.source) > 0:
            assign.is_trait = self.module.is_trait(assign.source)

        else:
            assign.is_trait = False

        for target in assign.targets:
            self.module.locals[target] = assign
            self.module.attributes[target] = assign
            self.module._is_trait[target] = assign.is_trait

        return

    def visit_ImportFrom(self, node):
        """ Visits a from node. """

        for alias in node.names:
            self.module.imports[alias.name] = node.module

        return

    def visit_Import(self, node):
        """ Visits an import node. """

        for alias in node.names:
            # fixme: We currently use the fact that we add an empty string to
            # the imports dictionary to tell the difference later on between
            # 'import' and 'from import'.
            self.module.imports[alias.name] = ''

        return

#### EOF ######################################################################
