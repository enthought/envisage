# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the 'Egg Basket' plugin manager. """

import glob
import shutil
import sys
import tempfile
import unittest
from os.path import basename, join

import pkg_resources

from envisage.egg_basket_plugin_manager import EggBasketPluginManager
from envisage.tests.test_egg_based import build_egg


class EggBasketPluginManagerTestCase(unittest.TestCase):
    """Tests for the 'Egg Basket' plugin manager."""

    #### 'unittest.TestCase' protocol #########################################

    @classmethod
    def setUpClass(cls):
        """
        Create eggs for testing purposes.
        """
        cls.eggs_dir = tempfile.mkdtemp()
        cls.bad_eggs_dir = tempfile.mkdtemp()

        eggs_root_dir = pkg_resources.resource_filename(
            "envisage.tests", "eggs"
        )
        for egg_name in ["acme-bar", "acme-baz", "acme-foo"]:
            build_egg(
                egg_dir=join(eggs_root_dir, egg_name),
                dist_dir=cls.eggs_dir,
            )

        bad_eggs_root_dir = pkg_resources.resource_filename(
            "envisage.tests", "bad_eggs"
        )
        for egg_name in ["acme-bad"]:
            build_egg(
                egg_dir=join(bad_eggs_root_dir, egg_name),
                dist_dir=cls.bad_eggs_dir,
            )

    @classmethod
    def tearDownClass(cls):
        """
        Delete created eggs.
        """
        shutil.rmtree(cls.bad_eggs_dir)
        shutil.rmtree(cls.eggs_dir)

    def setUp(self):
        """Prepares the test fixture before each test method is called."""

        # Some tests cause sys.path to be modified. Capture the original
        # contents so that we can restore sys.path later.
        self._original_sys_path_contents = sys.path[:]

    def tearDown(self):
        """Called immediately after each test method has been called."""

        # Undo any sys.path modifications
        sys.path[:] = self._original_sys_path_contents

        # `envisage.egg_utils.get_entry_points_in_egg_order` modifies the
        # global working set.
        pkg_resources.working_set = pkg_resources.WorkingSet()

    #### Tests ################################################################

    def test_find_plugins_in_eggs_on_the_plugin_path(self):
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.eggs_dir]
            )

        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 3)
        self.assertIn("acme.foo", ids)
        self.assertIn("acme.bar", ids)
        self.assertIn("acme.baz", ids)

    def test_only_find_plugins_whose_ids_are_in_the_include_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ["acme.foo", "acme.bar"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.eggs_dir], include=include
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.foo", "acme.bar"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_only_find_plugins_matching_a_wildcard_in_the_include_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        include = ["acme.b*"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.eggs_dir], include=include
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.bar", "acme.baz"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_ignore_plugins_whose_ids_are_in_the_exclude_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ["acme.foo", "acme.baz"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.eggs_dir], exclude=exclude
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.bar"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_ignore_plugins_matching_a_wildcard_in_the_exclude_list(self):
        # Note that the items in the list use the 'fnmatch' syntax for matching
        # plugins Ids.
        exclude = ["acme.b*"]

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.eggs_dir], exclude=exclude
            )

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.foo"]

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_reflect_changes_to_the_plugin_path(self):
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager()
        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 0)

        plugin_manager.plugin_path.append(self.eggs_dir)
        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 3)
        self.assertIn("acme.foo", ids)
        self.assertIn("acme.bar", ids)
        self.assertIn("acme.baz", ids)

        del plugin_manager.plugin_path[0]
        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 0)

    def test_ignore_broken_plugins_raises_exceptions_by_default(self):
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.bad_eggs_dir, self.eggs_dir],
            )
        with self.assertRaises(ImportError):
            list(plugin_manager)

    def test_ignore_broken_plugins_loads_good_plugins(self):
        data = {"count": 0}

        def on_broken_plugin(ep, exc):
            data["count"] += 1
            data["entry_point"] = ep
            data["exc"] = exc

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[self.bad_eggs_dir, self.eggs_dir],
                on_broken_plugin=on_broken_plugin,
            )

        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 3)
        self.assertIn("acme.foo", ids)
        self.assertIn("acme.bar", ids)
        self.assertIn("acme.baz", ids)

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["entry_point"].name, "acme.bad")
        exc = data["exc"]
        self.assertTrue(isinstance(exc, ImportError))

    def test_ignore_broken_distributions_raises_exceptions_by_default(self):
        # Make sure that the distributions from eggs are already in the working
        # set. This includes acme-foo, with version 0.1a1.
        for dist in pkg_resources.find_distributions(self.eggs_dir):
            pkg_resources.working_set.add(dist)

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[
                    # Attempt to add acme-foo, with conflicting version 0.1a11
                    self._create_broken_distribution_eggdir("acme_foo*.egg"),
                ],
            )
        with self.assertRaises(RuntimeError):
            iter(plugin_manager)

    def test_ignore_broken_distributions_loads_good_distributions(self):
        # Make sure that the distributions from eggs are already in the working
        # set. This includes acme-foo, with version 0.1a1.
        for dist in pkg_resources.find_distributions(self.eggs_dir):
            pkg_resources.working_set.add(dist)

        data = {"count": 0}

        def on_broken_distribution(dist, exc):
            data["count"] += 1
            data["distribution"] = dist
            data["exc"] = exc

        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggBasketPluginManager(
                plugin_path=[
                    self.eggs_dir,
                    self._create_broken_distribution_eggdir("acme_foo*.egg"),
                ],
                on_broken_distribution=on_broken_distribution,
            )

        ids = [plugin.id for plugin in plugin_manager]
        self.assertEqual(len(ids), 3)
        self.assertIn("acme.foo", ids)
        self.assertIn("acme.bar", ids)
        self.assertIn("acme.baz", ids)

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["distribution"].project_name, "acme-foo")
        exc = data["exc"]
        self.assertTrue(isinstance(exc, pkg_resources.VersionConflict))

    #### Private protocol #####################################################

    def _test_start_and_stop(self, plugin_manager, expected):
        """
        Make sure the plugin manager starts and stops the expected plugins.
        """

        # Make sure the plugin manager found only the required plugins.
        self.assertEqual(expected, [plugin.id for plugin in plugin_manager])

        # Start the plugin manager. This starts all of the plugin manager's
        # plugins.
        plugin_manager.start()

        # Make sure all of the the plugins were started.
        for id in expected:
            plugin = plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.started)

        # Stop the plugin manager. This stops all of the plugin manager's
        # plugins.
        plugin_manager.stop()

        # Make sure all of the the plugins were stopped.
        for id in expected:
            plugin = plugin_manager.get_plugin(id)
            self.assertNotEqual(None, plugin)
            self.assertEqual(True, plugin.stopped)

    def _create_broken_distribution_eggdir(self, egg_pat, replacement=None):
        """Copy a good egg to a different version egg name in a new temp dir
        and return the new directory.

        Parameters
        ----------
        egg_pat: a glob pattern for the egg in `self.egg_dir` eg 'foo.bar*.egg'
        replacement: a string replacement for the version part of egg name.
            If None, '1' is appended to the original version.

        Returns
        -------
        The newly created dir where the new broken egg is copied.
        Adding this dir to plugin_path will cause VersionConflict
        on trying to load distributions.
        """
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)

        # Copy the egg to the temp dir and rename it
        eggs = glob.glob(join(self.eggs_dir, egg_pat))
        for egg in eggs:
            egg_name = basename(egg)
            split_name = egg_name.split("-")
            if replacement is None:
                split_name[1] += "1"
            else:
                split_name[1] = replacement
            new_name = "-".join(split_name)
            shutil.copy(egg, join(tmpdir, new_name))

        return tmpdir
