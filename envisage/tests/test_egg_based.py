# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Base class for Egg-based test cases. """


import shutil
import subprocess
import sys
import tempfile
import unittest
from os.path import join

import pkg_resources


def build_egg(egg_dir, dist_dir):
    """Helper function to build an egg.

    Parameters
    ----------
    egg_dir : str
        Directory containing the Python package to be built. Should
        contain a "setup.py" file that can be used with
        "python setup.py bdist_egg" to build the package.
    dist_dir : str
        Directory to place the built egg in. The directory should
        already exist.
    """
    subprocess.run(
        [
            sys.executable,
            "setup.py",
            "bdist_egg",
            "--dist-dir",
            dist_dir,
        ],
        cwd=egg_dir,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class EggBasedTestCase(unittest.TestCase):
    """Base class for Egg-based test cases."""

    @classmethod
    def setUpClass(cls):
        """
        Create eggs for testing purposes.
        """
        cls.egg_dir = tempfile.mkdtemp()
        eggs_root_dir = pkg_resources.resource_filename(
            "envisage.tests", "eggs"
        )
        for egg_name in ["acme-bar", "acme-baz", "acme-foo"]:
            build_egg(
                egg_dir=join(eggs_root_dir, egg_name),
                dist_dir=cls.egg_dir,
            )

    @classmethod
    def tearDownClass(cls):
        """
        Delete created eggs.
        """
        shutil.rmtree(cls.egg_dir)

    def setUp(self):
        """Prepares the test fixture before each test method is called."""

        # Some tests cause sys.path to be modified. Capture the original
        # contents so that we can restore sys.path later.
        self._original_sys_path_contents = sys.path[:]

    def tearDown(self):
        """Called immediately after each test method has been called."""

        # Undo any sys.path modifications
        sys.path[:] = self._original_sys_path_contents

        pkg_resources.working_set = pkg_resources.WorkingSet()

    def _add_egg(self, filename, working_set=None):
        """Create and add a distribution from the specified '.egg'."""

        if working_set is None:
            working_set = pkg_resources.working_set

        # The eggs must be in our egg directory!
        filename = join(self.egg_dir, filename)

        # Create a distribution for the egg.
        distributions = pkg_resources.find_distributions(filename)

        # Add the distributions to the working set (this makes any Python
        # modules in the eggs available for importing).
        for distribution in distributions:
            working_set.add(distribution)

    def _add_eggs_on_path(self, path, working_set=None):
        """Add all eggs found on the path to a working set."""

        if working_set is None:
            working_set = pkg_resources.working_set

        environment = pkg_resources.Environment(path)

        # 'find_plugins' identifies those distributions that *could* be added
        # to the working set without version conflicts or missing requirements.
        distributions, errors = working_set.find_plugins(environment)
        # Py2 tests was checking that len(errors) > 0. This did not work on
        # Py3. Test changed to check the len(distributions)
        if len(distributions) == 0:
            raise RuntimeError("Cannot find eggs %s" % errors)

        # Add the distributions to the working set (this makes any Python
        # modules in the eggs available for importing).
        for distribution in distributions:
            working_set.add(distribution)
