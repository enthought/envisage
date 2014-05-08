""" An example of using the Enthought class browser (enclbr) module. """

# Future Statements
from __future__ import print_function
# Standard library imports.
import sys, time

# Enthought library imports.
from envisage.developer.code_browser.api import CodeBrowser


def main(argv):
    """ Do it! """

    if len(argv) != 2:
        print('Usage: python example.py module_name')
        print
        print('e.g., python example.py traits')

    else:
        # Create a code browser.
        code_browser = CodeBrowser(filename='data.pickle')

        # Parse the specified package.
        start = time.time()
        contents = code_browser.read_package(sys.argv[1])
        stop = time.time()

        print('Time taken to parse', sys.argv[1], 'was', stop - start, 'secs')

        # Save the cache.
        code_browser.save('data.pickle')

    return

# Entry point for testing.
if __name__ == '__main__':
    main(sys.argv)

#### EOF ######################################################################



