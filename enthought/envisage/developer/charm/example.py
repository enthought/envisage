""" An example of using the Enthought class browser (enclbr) module. """


# Standard library imports.
import sys, time

# Enthought library imports.
from enthought.charm import enclbr


def main(argv):
    """ Do it! """

    if len(argv) != 2:
        print 'Usage: python example.py module_name'
        print
        print 'e.g., python example.py enthought.traits'
        
    else:
        # Load the cache.
        enclbr.load_cache('data.pickle')
        
        # Parse the specified package.
        start = time.time()
        contents = enclbr.read_package(sys.argv[1])
        stop = time.time()
        
        print 'Time taken to parse', sys.argv[1], 'was', stop - start, 'secs'
        
        # Save the cache.
        enclbr.save_cache('data.pickle')

    return

# Entry point for testing.
if __name__ == '__main__':
    main(sys.argv)
    
#### EOF ######################################################################



