""" A Python namespace. """


# Standard library imports.
import os, sys

# Enthought library imports.
from traits.api import Dict, HasTraits


class Namespace(HasTraits):
    """ A Python namespace. """

    #### 'Namespace' interface ################################################

    # All of the names defined within the module.
    locals = Dict

    # All of the names imported into the module.
    imports = Dict

    # fixme: This is a dict from name -> bool indicating whether a name in
    # locals is a trait or not.  Should locals be a dict containing a tuple?
    _is_trait = Dict

    ###########################################################################
    # 'Namespace' interface.
    ###########################################################################

    def is_trait(self, name):
        """ Attempt to resolve a name to see if it is a trait. """

        # fixme: We might want to be a bit cleverer than this ;^)
        return True

        # Try the namespace's locals first.
        if name in self.locals:
            # These are the definitive traits markers!
            if name in ['TraitFactory', 'Trait', 'Instance']:
                is_trait = True

            # The name won't be in the '_is_trait' dictionary if it was not
            # defined by an assignment i.e., it is a class or function!
            elif not self._is_trait.get(name, False):
                is_trait = False

            else:
                next = self.locals[name]
                if len(next.source) > 0:
                    is_trait = self.is_trait(next.source)

                else:
                    is_trait = False

        # Is the name imported?
        elif self.is_imported(name):
            module_name = self.get_next_module_name(name)
            module = self.get_next_module(module_name)

            if module is not None:
                components = name.split('.')
                is_trait = module.is_trait(components[-1])

            else:
                is_trait = False

        # If we have a parent namespace then try that.
        elif self.namespace is not None:
            is_trait = self.namespace.is_trait(name)

        # Otherwise give up!
        else:
            is_trait = False

        return is_trait

    def is_imported(self, name):
        """ Returns TRUE if a name is imported. """

        components = name.split('.')

        return components[0] in self.imports

    def get_next_module_name(self, symbol):
        """ Returns the name of the module that a symbol was imported from. """

        components = symbol.split('.')
        if len(components) == 1:
            module_name = self.imports[symbol]

        else:
            path = []

            # The first component MUST have been imported.
            #
            # An empty string means 'import' as opposed to 'from' used.
            value = self.imports[components[0]]
            if len(value) > 0:
                path.append(value)

                module_name = '.'.join(path)

                return module_name

            path.append(components[0])

            for component in components[1:-1]:
                path.append(component)

            module_name = '.'.join(path)

        return module_name

    def get_next_module(self, module_name):
        """ Returns a parsed module with the specified name.

        Returns None if the module cannot be found or is 'ignored'.  We ignore
        all modules in the Python core, extension modules etc.

        """

        # fixme: Circular imports!
        from .enclbr import find_module, read_file

        # Try to find the module that the symbol came from.
        dirname = os.path.dirname(self.filename)
        filename = find_module(module_name, [dirname] + sys.path)

        if filename is not None:
            # If the filename refers to a directory then it must be a
            # package.
            if os.path.isdir(filename):
                filename = os.path.join(filename, '__init__.py')

            # fixme: We should probably put in some more formal filter
            # mechanism here!
            #
            # Ignore extension modules.
            if filename.endswith('.pyd') or filename.endswith('.so'):
                module = None

            # Ignore standard modules.
            elif filename.startswith(sys.prefix):
                module = None

            # Parse it!
            else:
                module = read_file(filename)

        else:
            module = None

        return module

#### EOF ######################################################################
