# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Tests for the Egg plugin manager. """

import contextlib
import os
import unittest

import pkg_resources
from pkg_resources import Environment, working_set

from envisage.api import EggPluginManager
from envisage.tests.support import (
    build_egg,
    PLUGIN_PACKAGES,
    restore_pkg_resources_working_set,
    restore_sys_modules,
    restore_sys_path,
    temporary_directory,
)


class EggPluginManagerTestCase(unittest.TestCase):
    """Tests for the Egg plugin manager."""

    @classmethod
    def setUpClass(cls):
        cls.egg_cleanup_stack = contextlib.ExitStack()
        cls.egg_dir = os.fspath(
            cls.egg_cleanup_stack.enter_context(temporary_directory())
        )

        # Build eggs
        for package in PLUGIN_PACKAGES:
            build_egg(package_dir=package, dist_dir=cls.egg_dir)

    @classmethod
    def tearDownClass(cls):
        cls.egg_cleanup_stack.close()

    def setUp(self):
        with contextlib.ExitStack() as cleanup_stack:
            cleanup_stack.enter_context(restore_sys_path())
            cleanup_stack.enter_context(restore_sys_modules())
            cleanup_stack.enter_context(restore_pkg_resources_working_set())
            self.addCleanup(cleanup_stack.pop_all().close)

        # Make eggs importable
        # 'find_plugins' identifies those distributions that *could* be added
        # to the working set without version conflicts or missing requirements.
        environment = Environment([os.fspath(self.egg_dir)])
        distributions, errors = working_set.find_plugins(environment)
        if len(distributions) == 0 or len(errors) > 0:
            raise RuntimeError(f"Cannot find eggs {errors}")
        for distribution in distributions:
            working_set.add(distribution)

    def test_no_include_or_exclude(self):
        """no include or exclude"""

        # Make sure that the plugin manager only includes those plugins.
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggPluginManager()

        # We don't know how many plugins we will actually get - it depends on
        # what eggs are on sys.path! What we *do* know however is the the 3
        # 'acme' test eggs should be in there!
        ids = [plugin.id for plugin in plugin_manager]

        self.assertTrue("acme.foo" in ids)
        self.assertTrue("acme.bar" in ids)
        self.assertTrue("acme.baz" in ids)

    def test_include_specific(self):
        """include specific"""

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.foo", "acme.bar"]

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = [r"acme\.foo", r"acme\.bar"]

        # Make sure that the plugin manager only includes those plugins.
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggPluginManager(include=include)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_include_multiple(self):
        """include multiple"""

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.foo", "acme.bar", "acme.baz"]

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ["acme.*"]

        # Make sure that the plugin manager only includes those plugins.
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggPluginManager(include=include)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_exclude_specific(self):
        """exclude specific"""

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.bar"]

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ["acme.*"]

        # Now exclude all but 'acme.bar'...
        exclude = [r"acme\.foo", r"acme\.baz"]

        # Make sure that the plugin manager excludes the specified plugins.
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggPluginManager(include=include, exclude=exclude)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_exclude_multiple(self):
        """exclude multiple"""

        # The Ids of the plugins that we expect the plugin manager to find.
        expected = ["acme.foo"]

        # We explicitly limit the plugins to be just the 'acme' test plugins
        # because otherwise the egg plugin manager will pick up *every* plugin
        # in *every* egg on sys.path!
        include = ["acme.*"]

        # Now exclude every plugin that starts with 'acme.b'.
        exclude = [r"acme\.b.*"]

        # Make sure that the plugin manager excludes the specified plugins.
        with self.assertWarns(DeprecationWarning):
            plugin_manager = EggPluginManager(include=include, exclude=exclude)

        # Make sure the plugin manager found only the required plugins and that
        # it starts and stops them correctly..
        self._test_start_and_stop(plugin_manager, expected)

    def test_uses_global_working_set_by_default(self):
        original_working_set = pkg_resources.working_set

        try:
            # Create fresh working set for this test, to make sure that the
            # plugin manager picks up the *current* value of
            # pkg_resources.working_set.
            fresh_working_set = pkg_resources.WorkingSet()
            pkg_resources.working_set = fresh_working_set
            with self.assertWarns(DeprecationWarning):
                plugin_manager = EggPluginManager()
            self.assertEqual(plugin_manager.working_set, fresh_working_set)
        finally:
            pkg_resources.working_set = original_working_set

    ###########################################################################
    # Private interface.
    ###########################################################################

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
