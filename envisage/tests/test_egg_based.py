# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Base class for Egg-based test cases. """


import pkg_resources
from os.path import dirname, join

from traits.testing.unittest_tools import unittest


class EggBasedTestCase(unittest.TestCase):
    """ Base class for Egg-based test cases. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # The location of the 'eggs' directory.
        self.egg_dir = join(dirname(__file__), 'eggs')

    def _add_egg(self, filename, working_set=None):
        """ Create and add a distribution from the specified '.egg'. """

        if working_set is None:
            working_set = pkg_resources.working_set

        # The eggs must be in our egg directory!
        filename = join(dirname(__file__), 'eggs', filename)

        # Create a distribution for the egg.
        distributions = pkg_resources.find_distributions(filename)

        # Add the distributions to the working set (this makes any Python
        # modules in the eggs available for importing).
        for distribution in distributions:
            working_set.add(distribution)

    def _add_eggs_on_path(self, path, working_set=None):
        """ Add all eggs found on the path to a working set. """

        if working_set is None:
            working_set = pkg_resources.working_set

        environment = pkg_resources.Environment(path)

        # 'find_plugins' identifies those distributions that *could* be added
        # to the working set without version conflicts or missing requirements.
        distributions, errors = working_set.find_plugins(environment)
        # Py2 tests was checking that len(errors) > 0. This did not work on
        # Py3. Test changed to check the len(distributions)
        if len(distributions) == 0:
            raise SystemError('Cannot find eggs %s' % errors)

        # Add the distributions to the working set (this makes any Python
        # modules in the eggs available for importing).
        for distribution in distributions:
            working_set.add(distribution)
