""" Tests for the resource manager. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.resource.api import ResourceManager
from enthought.traits.api import HasTraits, Int, Str


class ResourceManagerTestCase(unittest.TestCase):
    """ Tests for the resource manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_resource_manager(self):
        """ resource manager """

        rm = ResourceManager()

        # Open a file resources.
        f = rm.as_file('pkg_resource://enthought.envisage.resource:api.py')
        self.assertNotEqual(f, None)

        print f.read()
        
        return

#### EOF ######################################################################
