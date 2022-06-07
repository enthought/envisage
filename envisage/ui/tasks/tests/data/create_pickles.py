"""
Script to recreate the test pickles in this directory.

No arguments are required. Run with::

    $ python create_pickles.py
"""

import pathlib
import pickle

from envisage.ui.tasks.api import TasksApplicationState
from pyface.tasks.api import TaskWindowLayout

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
