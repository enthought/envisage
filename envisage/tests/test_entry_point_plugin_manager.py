# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

try:
    from importlib.metadata import EntryPoint, EntryPoints
except ImportError:
    from importlib_metadata import EntryPoint, EntryPoints

import unittest

from envisage.core_plugin import CorePlugin
from envisage.entry_point_plugin_manager import EntryPointPluginManager
from envisage.i_plugin_manager import IPluginManager
from envisage.plugin import Plugin
from envisage.tests.support import event_recorder


class BaseInstrumentedPlugin(Plugin):
    """
    A plugin that records its start and stop to the global event_recorder.
    """
    def start(self):
        event_recorder.record(("starting", self.id))

    def stop(self):
        event_recorder.record(("stopping", self.id))


class SpyPlugin(BaseInstrumentedPlugin):
    id = "SpyPlugin"


class AnotherSpyPlugin(BaseInstrumentedPlugin):
    id = "AnotherSpyPlugin"


class TestEntryPointPluginManager(unittest.TestCase):
    def test_implements_interface(self):
        self.assertIsInstance(EntryPointPluginManager(), IPluginManager)

    def test_using_entry_points(self):
        # Given a collection of entry points referring to plugins ...
        entry_points = EntryPoints(
            EntryPoint(group="myapp.plugins", name=name, value=value)
            for name, value in [
                ("spy_plugin", f"{__name__}:SpyPlugin"),
                ("another_spy_plugin", f"{__name__}:AnotherSpyPlugin"),
            ]
        )

        # ... and a manager that uses them
        manager = EntryPointPluginManager(entry_points=entry_points)

        # When we start and stop the manager
        with event_recorder.start_recording() as events:
            manager.start()
            manager.stop()

        # Then the expected plugins are started and stopped.
        self.assertEqual(
            events,
            [
                ("starting", "SpyPlugin"),
                ("starting", "AnotherSpyPlugin"),
                ("stopping", "AnotherSpyPlugin"),
                ("stopping", "SpyPlugin"),
            ],
        )

    def test_global_entry_points_selected_by_group(self):
        # Given a manager that selects entry points from the Python environment
        manager = EntryPointPluginManager(group="envisage.plugins")

        # When we retrieve the list of plugins
        plugins = list(manager)

        # Then we get the expected plugins (in this case, a single CorePlugin
        # instance).
        self.assertEqual(len(plugins), 1)
        self.assertIsInstance(plugins[0], CorePlugin)
