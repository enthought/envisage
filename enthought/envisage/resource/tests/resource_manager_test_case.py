""" Tests for the resource manager. """


# Standard library imports.
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os, thread, time, unittest

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

    def test_package_resource(self):
        """ package resource """

        rm = ResourceManager()

        # Open a package resource.
        f = rm.file('package://enthought.envisage.resource/api.py')
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()
        
        # Open the api file via the file system (we open in binary mode because
        # that is what pkg_resources does, and otherwise the line endings get
        # converted).
        g = file('../api.py', 'rb')
        self.assertEqual(g.read(), contents)
        g.close()

        return

##     def test_http_resource(self):
##         """ HTTP resource """

##         rm = ResourceManager()

##         # Open an HTTP document resource.
##         f = rm.file('http://code.enthought.com')
##         self.assertNotEqual(f, None)
##         contents = f.read()
##         f.close()

##         # I tried to pick a bit of the document that shouldn't change too much!
##         self.assert_('<title>code.enthought.com - Home</title>' in contents)
        
##         return

    def test_http_resource(self):
        """ http uol """

        # We will publish the current time!
        t = str(time.time())

        # Write the time to a file.
        f = file('time.dat', 'w')
        f.write(t)
        f.close()

        # Offer the file via http!
        httpd = HTTPServer(('localhost', 1234), SimpleHTTPRequestHandler)
        thread.start_new_thread(httpd.serve_forever, ())

        # Open an HTTP document resource.
        rm = ResourceManager()

        f = rm.file('http://localhost:1234/time.dat')
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()

        self.assertEquals(contents, t)

        # Cleanup.
        os.remove('time.dat')
        
        return

#### EOF ######################################################################
