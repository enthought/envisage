Welcome to the "Message of the Day" (MOTD) example.

This directory contains two subdirectories::

dist
  Which contains the actual runnable application as it might actually be
  distributed/deployed.

src
  Which contains the source code for the eggs that make up the application.
  This directory is there to allow easy access to the example code, but would
  obviously not normally be deployed.

To build the eggs required by the application:: (where, '...' refers to the
directory that *this* file is in)::

  ``cd .../src/acme.motd``
  ``python setup.py bdist_egg -d ../../dist/eggs``

  ``cd .../src/acme.motd.software_quotes``
  ``python setup.py bdist_egg -d ../../dist/eggs``

To run the application::

  ``cd .../dist``
  ``python run.py``

  or equivalent, depending on your operating system and shell.

