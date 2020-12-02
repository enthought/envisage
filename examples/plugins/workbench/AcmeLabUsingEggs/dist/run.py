""" Run the application.

Usually, all you have to do in here is:-

1) Initialise the logging package as you see fit (or not at all ;^)!

2) Set the 'EGG_PATH' variable to be a list of the directories that contain
   your application's eggs.

3) Edit the 'run' function to do whatever you need to do to start your
   application.

"""


# Standard library imports.
import logging


# Create a log file.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(file('acmelab.log', 'w')))
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# A list of the directories that contain the application's eggs (any directory
# not specified as an absolute path is treated as being relative to the current
# working directory).
EGG_PATH = ['eggs']


def run():
    """ The function that starts your application. """

    # We do the imports here because the modules may well be in eggs that get
    # added to the path in 'main'.
    from envisage.api import EggPluginManager
    from acme.acmelab.api import Acmelab

    # Create an application that uses the egg plugin manager to find its
    # plugins.
    acmelab = Acmelab(plugin_manager=EggPluginManager())

    # Run it! This starts the application, starts the GUI event loop, and when
    # that terminates, stops the application.
    return acmelab.run()


###############################################################################
# Usually, there is no need to edit anything below here!
###############################################################################

# Standard library imports.
import logging
from pkg_resources import Environment, working_set


# Logging.
logger = logging.getLogger(__name__)


def main():
    """ Run the application. """

    # Find all additional eggs.
    environment = Environment(EGG_PATH)

    distributions, errors = working_set.find_plugins(environment)
    if len(errors) > 0:
        raise SystemError('cannot add eggs %s' % errors)

    logger.debug('added eggs %s' % distributions)

    # Add them to the working set.
    map(working_set.add, distributions)

    # Create and run the application.
    return run()


if __name__ == '__main__':
    main()

#### EOF ######################################################################
