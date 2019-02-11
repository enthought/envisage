This directory contains eggs used by the test suite, along with the packages
that were used to generate those eggs.

To generate eggs for a new version of Python:

- Change to the acme.bar directory
- Run "python setup.py bdist_egg" using the desired version of Python. This
  will create a new egg under the "dist/" directory.
- Copy that egg to this directory.

Now repeat for acme.baz and acme.foo, as well as acme.bad in the bad_eggs
directory adjacent to this one.
