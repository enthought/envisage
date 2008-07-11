""" Run the application.

Usually, all you have to do in here is:-

1) Initialise the logging package as you see fit (or not at all ;^)!

2) Set the 'EGG_PATH' variable to be a list of the directories that contain
   your application's eggs.

3) Edit the 'run' function to do whatever you need to do to start your
   application.

"""
# FIXME: This fix will work for now, but I believe there is a better way to do
# this in which the loader would be smart enough to know what plugins it should
# load without having to explicitly define them in 'include'. Also, the custom
# __plugin_default method now looks at the entry point name instead of the
# plugin.id, which is less specific therefore less preferable. This was done,
# however, because the ep.name can be accessed before the ep.load() call, which
# was causing problems when loading plugins not designed for this app. (dmartin)

# Standard library imports.
import logging

# Enthought linrary imports
from enthought.envisage.api import Application, EggPluginManager
from enthought.envisage.egg_utils import get_entry_points_in_egg_order

# Create a log file.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(file('acme_motd.log', 'w')))
logger.setLevel(logging.DEBUG)

# A list of the directories that contain the application's eggs (any directory
# not specified as an absolute path is treated as being relative to the current
# working directory).
EGG_PATH = ['eggs']

class MOTDPluginManager(EggPluginManager):
    """ A plugin manager that will get only the MOTD eggs """

    # Only include the plugins necessary for the example
    include = ['core', 'motd', 'software_quotes']

    # Use a custom plugin loader that will NOT attempt to execute a .load on
    # every plugin, therefore avoiding any errors that unwanted plugins may
    # cause. Only execute a .load on entry points that are given in 'include'
    def __plugins_default(self):
        """ Trait initializer. """

        plugins = []
        for ep in get_entry_points_in_egg_order(self.working_set,self.PLUGINS):
            if ep.name in self.include:
                klass  = ep.load()
                plugin = klass(application=self.application)
                plugins.append(plugin)

        logger.debug('motd plugin manager found plugins <%s>', plugins)

        return plugins

def run():
    """ The function that starts your application. """

    # Create an application that uses the egg plugin manager to find its
    # plugins.
    application = Application(id='acme.motd',plugin_manager=MOTDPluginManager())

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
