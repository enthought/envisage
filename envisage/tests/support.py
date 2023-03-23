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

import unittest

from pyface.api import GUI
from traits.api import Int, List

from envisage.api import Application, ExtensionPoint, Plugin

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
    pyside6_version = None
else:
    pyside6_available = True
    pyside6_version = PySide6.__version_info__
    del PySide6


# Application class used in various tests.


class SimpleApplication(Application):
    """The type of application used in the tests."""

    id = "test"


# Plugins used in multiple tests.


class PluginA(Plugin):
    """A plugin that offers an extension point."""

    id = "A"
    x = ExtensionPoint(List, id="a.x")


class PluginB(Plugin):
    """A plugin that contributes to an extension point."""

    id = "B"
    x = List(Int, [1, 2, 3], contributes_to="a.x")


class PluginC(Plugin):
    """Another plugin that contributes to an extension point!"""

    id = "C"
    x = List(Int, [98, 99, 100], contributes_to="a.x")
