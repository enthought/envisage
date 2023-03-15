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
import contextlib

from traits.api import Event

from envisage.plugin import Plugin
from envisage.entry_point_plugin_manager import EntryPointPluginManager
from envisage.i_plugin_manager import IPluginManager


# XXX Move the EventRecorder to test support?

# 'event_recorder' is a piece of global state that lets us record plugin start
# and stop events.

class EventRecorder:
    @contextlib.contextmanager
    def record_to(self, target_list):
        self._events = target_list
        try:
            yield
        finally:
            del self._events

    def record(self, event):
        if not hasattr(self, "_events"):
            raise RuntimeError(
                "No target list for recording. Set a target list using "
                "the 'record_to' context manager."
            )
        self._events.append(event)


event_recorder = EventRecorder()


# Instrumented plugins


class BaseInstrumentedPlugin(Plugin):
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

    def test_entry_points_directly_specified(self):

        # Name of the entry points group that we'll use for testing.
        group = "myapp.plugins"

        # No good - we need to run in the target environment.
        # Can we fake it for now, then add integration tests later?

        # Entry points in the (mocked) environment.
        # Triples (entry point group name, entry point name, object reference)
        entry_points = EntryPoints(
            EntryPoint(group=group, name=name, value=value)
            for name, value in [
                ("spy_plugin", "envisage.tests.test_entry_point_plugin_manager:SpyPlugin"),
                ("another_spy_plugin", "envisage.tests.test_entry_point_plugin_manager:AnotherSpyPlugin"),
            ]
        )

        # XXX Add other entry points that aren't plugins; check that they
        # aren't picked up.

        manager = EntryPointPluginManager(entry_points=entry_points)

        events = []
        with event_recorder.record_to(events):
            manager.start()
            manager.stop()

        self.assertEqual(
            events,
            [('starting', 'SpyPlugin'), ('starting', 'AnotherSpyPlugin'), ('stopping', 'AnotherSpyPlugin'), ('stopping', 'SpyPlugin')],
        )

    def test_select_by_group(self):
        manager = EntryPointPluginManager(group="envisage.plugins")

        breakpoint()
