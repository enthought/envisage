# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Utilities for supporting Envisage's demo examples.
"""

import contextlib
import os
import sys


@contextlib.contextmanager
def demo_path(path):
    """Context manager to temporarily insert the directory containing
    the demo script to sys.path such that demo examples can be run using
    local packages.

    This function should only be used by Envisage example files.

    Parameters
    ----------
    path : Path-like
        Path to the demo script to be run.
    """
    path = os.path.dirname(os.fspath(path))
    try:
        sys.path.insert(0, path)
        yield
    finally:
        sys.path.remove(path)
