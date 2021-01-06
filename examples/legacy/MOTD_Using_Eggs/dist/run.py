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
logger.addHandler(logging.StreamHandler(file('acme_motd.log', 'w')))
logger.setLevel(logging.DEBUG)


# A list of the directories that contain the application's eggs (any directory
# not specified as an absolute path is treated as being relative to the current
# working directory).
EGG_PATH = ['eggs']


def run():
    """ The function that starts your application. """

    # Enthought library imports.
    #
    # We do the imports here in case the Enthought eggs are loaded dyanmically
    # via the 'EGG_PATH'.
    from envisage.api import Application, EggPluginManager

    # Create a plugin manager that ignores all eggs except the ones that we
    # need for this example.
    plugin_manager = EggPluginManager(
        include = [
            'envisage.core', 'acme.motd', 'acme.motd.software_quotes'
        ]
    )

    # Create an application that uses the egg plugin manager to find its
    # plugins.
    application = Application(id='acme.motd', plugin_manager=plugin_manager)

    # Run it!
    return application.run()


###############################################################################
# Usually, there is no need to edit anything below here!
###############################################################################

# Standard library imports.
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
