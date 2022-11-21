This directory contains data files used in tests.

- application_memento_v2.pkl is a pickled TasksApplicationState
  object containing layout information. It's pickled using pickle
  protocol 2.
- application_memento_v3.pkg pickles the same object as above,
  but using pickle protocol 3.
- create_pickles.py is a script that can be run to regenerate the
  above pickle files.
