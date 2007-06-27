""" Base class for Egg-based test cases. """


# Standard library imports.
import unittest
import pkg_resources
from os.path import dirname, join
from pkg_resources import Distribution, Environment, find_distributions


class EggBasedTestCase(unittest.TestCase):
    """ Base class for Egg-based test cases. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # The location of the 'eggs' directory.
        self.egg_dir = join(dirname(__file__), 'eggs')
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_egg(self, filename, working_set=None):
        """ Create and add a distribution from the specified '.egg'. """

        working_set = working_set or pkg_resources.working_set

        # The eggs must be in our egg directory!
        filename = join(dirname(__file__), 'eggs', filename)
        
        # fixme: This way doesn't work - why not?!?
        #
        # distribution = Distribution.from_filename(filename)
        # working_set.add(distribution)
        distributions = find_distributions(filename)

        # Add the distributions to the working set (this makes any Python
        # modules in the eggs available for importing).
        map(working_set.add, distributions)

        return
    
    def _add_eggs_on_path(self, path, working_set=None):
        """ Add all eggs found on the path to a working set. """

        working_set = working_set or pkg_resources.working_set

        environment = Environment(path)
        
        # 'find_plugins' identifies those distributions that *could* be added
        # to the working set without version conflicts or missing requirements.
        distributions, errors = working_set.find_plugins(environment)

        # fixme: Log the errors...

        # Add the distributions to the working set (this makes any Python
        # modules in the eggs available for importing).
        map(working_set.add, distributions)

        return

#### EOF ######################################################################
