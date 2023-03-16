# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Support utilities for tests in the Envisage test suite.

Note: this is intended to provide helpers for testing Envisage itself rather
than for external Envisage-based code. The helpers here should be considered
private to Envisage.
"""

import contextlib
import unittest

from pyface.api import GUI

# Skip decorator for tests that require a working GUI instance.
try:
    GUI()
except NotImplementedError:
    gui_available = False
else:
    gui_available = True

requires_gui = unittest.skipUnless(
    gui_available, "Test requires a non-null GUI backend"
)


# Test for PySide6 being installed
try:
    import PySide6
except ImportError:
    pyside6_available = False
else:
    pyside6_available = True
    del PySide6


# 'event_recorder' is an evil piece of global state that lets us record events
# in situations where we don't have direct access to the objects that are
# generating those events.


class _EventRecorder:
    """
    Object that can temporary send events to any particular list.

    Examples
    --------

    Use as follows::

        my_events = []
        with event_recorder.record_to(my_events):
            <do stuff that calls event_recorder.record>

        <inspect contents of my_events>

    """

    @contextlib.contextmanager
    def start_recording(self, target_list=None):
        """
        Context manager that records events for the duration of the context.

        Yields the list being recorded to.
        """
        if hasattr(self, "_events"):
            raise RuntimeError("start_recording calls cannot be nested")

        if target_list is None:
            target_list = []

        self._events = target_list
        try:
            yield target_list
        finally:
            del self._events

    def record(self, event):
        """
        Record an 'event' (which can be any Python object).

        May only be used within a 'start_recording' context.
        """
        if not hasattr(self, "_events"):
            raise RuntimeError(
                "The 'record' method may only be called within a "
                "start_recording context."
            )
        self._events.append(event)


event_recorder = _EventRecorder()
