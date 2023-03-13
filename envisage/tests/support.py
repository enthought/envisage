"""
Support utilities for tests in the Envisage test suite.

Note: this is intended to provide helpers for testing Envisage itself rather
than for external Envisage-based code. The helpers here should be considered
private to Envisage.
"""

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
