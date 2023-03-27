# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Base class for Egg-based test cases.

The egg-based test cases make significant changes to global state, so we need
to work to undo those global state changes and ensure test independence.
"""

import contextlib
import pathlib
import subprocess
import sys
import tempfile

from pkg_resources import working_set


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
    original_normalized = set(working_set.normalized_to_canonical_keys)
    try:
        yield
    finally:
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
