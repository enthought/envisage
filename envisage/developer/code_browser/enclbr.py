""" The Enthought class browser module. """


# Standard library imports.
import imp, logging, os, stat, warnings

# Enthought library imports.
from apptools.io.api import File

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


# A cache that contains every module that has been parsed.
MODULES = {}

# Has the cache been modified in this process?
MODULES_CHANGED = False


def save_cache(filename):
    """ Saves the module cache to disk. """

    global MODULES
    global MODULES_CHANGED

    if MODULES_CHANGED:
        logger.debug('saving cache...')

        f = open(filename, 'wb')
        pickle.dump(MODULES, f, 1)
        f.close()

        logger.debug('cache saved')

    return


def load_cache(filename):
    """ Loads the module cache from disk. """

    global MODULES

    if os.path.isfile(filename):
        logger.debug('loading cache...')

        f = open(filename, 'rb')
        MODULES = pickle.load(f)
        f.close()

        logger.debug('cache loaded...')

    else:
        MODULES = {}

    return


def read_package(package_name):
    """ Parse every module in the specified package. """

    filename = find_module(package_name)
    if filename is None:
        raise ValueError("no such package '%s'" % package_name)

    package = Package(filename=filename, name=package_name)
    read_directory(filename, package)

    return package


def read_directory(filename, package=None):
    """ Parse every module in the specified directory. """

    directory = File(filename)
    if not directory.is_folder:
        raise ValueError("%s is NOT a directory." % filename)

    if package is not None:
        contents = package.contents

    else:
        contents = []

    for child in directory.children:
        if child.ext == '.py':
            contents.append(read_file(child.path, package))

        elif child.is_package:
            if package is not None:
                sub_package_name = '%s.%s' % (package.name, child.name)
                sub_package = Package(
                    filename=child.path, name=sub_package_name, parent=package
                )

            else:
                sub_package = Package(filename=child.path, name=child.name)

            read_directory(child.path, sub_package)
            contents.append(sub_package)

    return contents


def read_file(filename, namespace=None):
    """ Parses a file. """

    global MODULES
    global MODULES_CHANGED

    module, mod_time = MODULES.get(filename, (None, None))
    if module is None or mod_time != os.stat(filename)[stat.ST_MTIME]:
        logger.debug('parsing module %s' % filename)

        module_factory = ModuleFactory()
        try:
            module = module_factory.from_file(filename, namespace)

            # Add the parsed module to the cache.
            MODULES[filename] = (module, os.stat(filename)[stat.ST_MTIME])
            MODULES_CHANGED = True

        except:
            logger.exception('error parsing file %s' % filename)

    return module


def read_module(module_name):
    """ Parses a module. """

    filename = find_module(module_name)
    if filename is not None:
        module = read_file(filename)

    else:
        module = None

    return module


def find_module(module_name, path=None):
    """ Returns the filename for the specified module. """

    components = module_name.split('.')

    try:
        # Look up the first component of the module name (of course it could be
        # the *only* component).
        f, filename, description = imp.find_module(components[0], path)

        # If the module is in a package then go down each level in the package
        # hierarchy in turn.
        if len(components) > 0:
            for component in components[1:]:
                f,filename,description = imp.find_module(component, [filename])

    except ImportError:
        filename = None

    return filename

#### EOF ######################################################################
