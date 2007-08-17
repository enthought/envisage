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
        f = rm.file('package://enthought.envisage.resource/api.py')
        self.assertNotEqual(f, None)

        contents = f.read()
        f.close()
        
        # Open the api file via the file system (we open in binary mode because
        # that is what pkg_resources does).
        g = file('../api.py', 'rb')
        self.assertEqual(g.read(), contents)
        g.close()
        
        return

#### EOF ######################################################################
