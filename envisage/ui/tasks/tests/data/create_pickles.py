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
Script to recreate the test pickles in this directory.

No arguments are required. Run with::

    $ python create_pickles.py
"""

import pathlib
import pickle

from pyface.tasks.api import TaskWindowLayout

from envisage.ui.tasks.api import TasksApplicationState

state = TasksApplicationState(
    version=1,
    window_layouts=[],
    previous_window_layouts=[
        TaskWindowLayout(size=(492, 743)),
    ],
)

v2_pkl = pathlib.Path("application_memento_v2.pkl")
v3_pkl = pathlib.Path("application_memento_v3.pkl")

v2_pkl.write_bytes(pickle.dumps(state, protocol=2))
v3_pkl.write_bytes(pickle.dumps(state, protocol=3))
