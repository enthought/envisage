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
import pathlib
import subprocess
import sys
import tempfile
import unittest

from pkg_resources import resource_filename, working_set

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


# Various useful context managers.


@contextlib.contextmanager
def temporary_directory():
    """
    Create and remove a temporary directory.

    Yields a pathlib.Path instance.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        yield pathlib.Path(tempdir)


@contextlib.contextmanager
def restore_sys_path():
    """
    Save and restore `sys.path` state.

    On entering the associated context, this context manager saves the state of
    `sys.path`. Within the context, code may then make changes to that global
    state (for example by adding distributions to the working set). On exiting
    the context, `sys.path` is restored to its original state.
    """
    original_sys_path = sys.path[:]
    try:
        yield
    finally:
        sys.path[:] = original_sys_path


@contextlib.contextmanager
def restore_sys_modules():
    """
    Save and restore `sys.modules` state.

    On entering the associated context, this context manager saves the state of
    `sys.modules`. On exiting the context, any additional keys that were added
    to `sys.modules` are removed.
    """
    original_modules = set(sys.modules)
    try:
        yield
    finally:
        for name in sys.modules.keys() - original_modules:
            del sys.modules[name]


@contextlib.contextmanager
def restore_pkg_resources_working_set():
    """
    Save and restore `pkg_resources.working_set` state.

    On entering the associated context, this context manager saves the state of
    `pkg_resources.working_set`. Within the context, code may then make changes
    to that global state (for example by adding distributions to the working
    set). On exiting the context, `pkg_resources.working_set` is restored to
    its original state.
    """
    original_entries = working_set.entries[:]
    original_entry_keys = set(working_set.entry_keys)
    original_by_key = set(working_set.by_key)
    # Older setuptools versions don't have this attribute; it appears to
    # be new in setuptools ~ 62.
    if hasattr(working_set, "normalized_to_canonical_keys"):
        original_normalized = set(working_set.normalized_to_canonical_keys)
    else:
        original_normalized = None
    try:
        yield
    finally:
        if original_normalized is not None:
            for key in (
                working_set.normalized_to_canonical_keys.keys()
                - original_normalized
            ):
                del working_set.normalized_to_canonical_keys[key]
        for key in working_set.by_key.keys() - original_by_key:
            del working_set.by_key[key]
        for key in working_set.entry_keys.keys() - original_entry_keys:
            del working_set.entry_keys[key]
        working_set.entries[:] = original_entries


# Egg and package-related functionality.


def build_egg(package_dir, dist_dir):
    """Helper function to build an egg.

    Parameters
    ----------
    package_dir : pathlib.Path
        Directory containing the Python package to be built. Should
        contain a "setup.py" file that can be used with
        "python setup.py bdist_egg" to build the package.
    dist_dir : pathlib.Path
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
        cwd=package_dir,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


# Packages containing plugins that are used for testing

_PACKAGES_DIR = pathlib.Path(resource_filename("envisage.tests", "eggs"))
PLUGIN_PACKAGES = [
    _PACKAGES_DIR / "acme-bar",
    _PACKAGES_DIR / "acme-baz",
    _PACKAGES_DIR / "acme-foo",
]

# acme-bad contains a plugin that depends on a non-existent module.
_BAD_PACKAGES_DIR = pathlib.Path(
    resource_filename("envisage.tests", "bad_eggs")
)
BAD_PLUGIN_PACKAGES = [_BAD_PACKAGES_DIR / "acme-bad"]


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
