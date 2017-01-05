""" A simple traits-aware code browser. """


# Standard library imports.
import imp, logging, os, stat, warnings

# Enthought library imports.
from apptools.io.api import File
from traits.api import Any, Bool, Event, HasTraits, Str

# Local imports.
from .module import ModuleFactory
from .package import Package
from ..._compat import pickle

# Logging.
logger = logging.getLogger(__name__)


# Filter future warnings for maxint, since it causes warnings when compiling
# anything that has RGBA colors defined as hex values.
warnings.filterwarnings(
    "ignore", r'hex/oct constants > sys\.maxint .*', FutureWarning
)


class CodeBrowser(HasTraits):
    """ A simple, traits-aware code browser. """

    #### 'ClassBrowser' interface #############################################

    # The filename of the (optional, persistent) code 'database'.
    filename = Str

    #### Events ####

    # Fired when a module is about to be parsed.
    parsing_module = Event

    # Fired when a module has been parsed.
    parsed_module = Event

    #### Private interface ####################################################

    # The code 'database' that contains every module that has been parsed.
    _database = Any

    # Has the code database been changed (i.e., do we need to save it)?
    _database_changed = Bool(False)

    ###########################################################################
    # 'CodeBrowser' interface.
    ###########################################################################

    def load(self):
        """ Load the code browser 'database'. """

        # If a persisted code database exists then load it...
        if os.path.isfile(self.filename):
            logger.debug('loading code database...')

            f = open(self.filename, 'rb')
            self._database = pickle.load(f)
            f.close()

            logger.debug('code database loaded.')

        # ... otherwise we have a nice, fresh and very empty database.
        else:
            self._database = {}

        return

    def save(self):
        """ Save the code browser 'database' to disk. """

        if self._database_changed:
            logger.debug('saving code database...')

            f = open(self.filename, 'wb')
            pickle.dump(self._database, f, 1)
            f.close()

            self._database_changed = False

            logger.debug('code database saved.')

        else:
            logger.debug('code database unchanged - nothing saved.')

        return

    def read_package(self, package_name):
        """ Parse every module in the specified package. """

        filename = self.find_module(package_name)
        if filename is None:
            raise ValueError("no such package '%s'" % package_name)

        package = Package(filename=filename, name=package_name)
        self.read_directory(filename, package)

        return package

    def read_directory(self, filename, package=None):
        """ Parse every module in the specified directory. """

        directory = File(filename)
        if not directory.is_folder:
            raise ValueError("%s is NOT a directory." % filename)

        if package is not None:
            contents = package.contents

        else:
            contents = []

        for child in directory.children:
            # If the child is a Python file then parse it.
            if child.ext == '.py':
                contents.append(self.read_file(child.path, package))

            # If the child is a sub-package then recurse!
            elif child.is_package:
                if package is not None:
                    sub_package_name = '%s.%s' % (package.name, child.name)
                    sub_package = Package(
                        filename = child.path,
                        name     = sub_package_name,
                        parent   = package
                    )

                else:
                    sub_package = Package(filename=child.path, name=child.name)

                self.read_directory(child.path, sub_package)
                contents.append(sub_package)

        return contents

    def read_file(self, filename, namespace=None):
        """ Parse a file. """

        # Only parse the file if we haven't parsed it before or it has been
        # modified since we last parsed it!
        module, mod_time = self._database.get(filename, (None, None))
        if module is None or mod_time != os.stat(filename)[stat.ST_MTIME]:
            # Event notification.
            self.parsing_module = filename
            logger.debug('parsing module %s' % filename)

            module_factory = ModuleFactory()
            try:
                module = module_factory.from_file(filename, namespace)

                # Event notification.
                self.parsed_module = module
                logger.debug('parsed module %s' % filename)

                # Add the parsed module to the database.
                self._database[filename] = (
                    module, os.stat(filename)[stat.ST_MTIME]
                )
                self._database_changed = True

            except SyntaxError:
                logger.debug('error parsing module %s' % filename)

        return module

##     def read_module(self, module_name):
##         """ Parses a module. """

##         filename = self.find_module(module_name)
##         if filename is not None:
##             module = self.read_file(filename)

##         else:
##             module = None

##         return module

    def find_module(self, module_name, path=None):
        """ Return the filename for the specified module. """

        components = module_name.split('.')

        try:
            # Look up the first component of the module name (of course it
            # could be the *only* component).
            f, filename, description = imp.find_module(components[0], path)

            # If the module is in a package then go down each level in the
            # package hierarchy in turn.
            if len(components) > 0:
                for component in components[1:]:
                    f, filename, description = imp.find_module(
                        component, [filename]
                    )

        except ImportError:
            filename = None

        return filename

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def __database_default(self):
        """ Trait initializer. """

        return {}

    #### Trait change handlers ################################################

    def _filename_changed(self):
        """ Called when the filename of the code database is changed. """

        # Load the contents of the database.
        self.load()

        return

#### EOF ######################################################################
