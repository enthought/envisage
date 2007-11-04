Welcome to the "Message of the Day" (MOTD) example.

This directory contains two subdirectories::

dist
  Which contains the actual runnable application as it might actually be
  distributed/deployed.

To build the eggs required by the application::

  ``cd .../examples/MOTD/src/acme.motd``
  ``python setup.py bdist_egg -d ../../dist/eggs``

  ``cd .../examples/MOTD/src/acme.motd.software_quotes``
  ``python setup.py bdist_egg -d ../../dist/eggs``

  To run the application::

  ``cd .../examples/MOTD/dist``
  ``python run.py``
  
  or equivalent, depending on your operating system and shell.
  
src
  Which contains the source code for the eggs that make up the application.
  This directory is there to allow easy access to the example code, but would
  obviously not normally be deployed.

