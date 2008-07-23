""" Tests for the resource manager. """


# Standard library imports.
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os, tempfile, thread, time, unittest
from os.path import join

# Major package imports.
from pkg_resources import resource_filename

# Enthought library imports.
from enthought.envisage.resource.api import ResourceManager
from enthought.envisage.resource.api import NoSuchResourceError
from enthought.traits.api import HasTraits, Int, Str

from enthought.util.resource import find_resource


# This module's package.
PKG = 'enthought.envisage.resource.tests'


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
    
    def test_file_resource(self):
        """ file resource """

        rm = ResourceManager()

        # Get the filename of the 'api.py' file.
        filename = resource_filename('enthought.envisage.resource', 'api.py')
        
        # Open a file resource.
        f = rm.file('file://' + filename)
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()
        
        # Open the api file via the file system.
        g = file(filename, 'rb')
        self.assertEqual(g.read(), contents)
        g.close()
        
        return
    
    def test_no_such_file_resource(self):
        """ no such file resource """

        rm = ResourceManager()

        # Open a file resource.
        self.failUnlessRaises(
            NoSuchResourceError, rm.file, 'file://../bogus.py'
        )

        return

    def test_package_resource(self):
        """ package resource """

        rm = ResourceManager()

        # Open a package resource.
        f = rm.file('pkgfile://enthought.envisage.resource/api.py')
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()
        
        # Get the filename of the 'api.py' file.
        filename = resource_filename('enthought.envisage.resource', 'api.py')

        # Open the api file via the file system.
        g = file(filename, 'rb')
        self.assertEqual(g.read(), contents)
        g.close()

        return

    def test_no_such_package_resource(self):
        """ no such package resource """

        rm = ResourceManager()

        # Open a package resource.
        self.failUnlessRaises(
            NoSuchResourceError,
            rm.file,
            'pkgfile://enthought.envisage.resource/bogus.py'
        )

        self.failUnlessRaises(
            NoSuchResourceError, rm.file, 'pkgfile://completely.bogus/bogus.py'
        )

        return

    # fixme: This test fails when port 1234 is already in use.
    def test_http_resource(self):
        """ http resource """
        
        # fixme: We should not write to the local directory here, but to use
        # a 'tempfile' we would have to create a new request handler which
        # seems like a bit of a pain!
        ##tmpdir = tempfile.mkdtemp()

        # A temporary file.
        ##tmp = join(tmpdir, 'time.dat')
        tmp = 'time.dat'
        
        # We will publish the current time!
        t = str(time.time())

        # Write the time to a file.
        f = file(tmp, 'w')
        f.write(t)
        f.close()

        try:
            # Offer the file via http!
            httpd = HTTPServer(('localhost', 1234), SimpleHTTPRequestHandler)
            thread.start_new_thread(httpd.handle_request, ())
            
            # Open an HTTP document resource.
            rm = ResourceManager()

            f = rm.file('http://localhost:1234/%s' % tmp)
            self.assertNotEqual(f, None)
            contents = f.read()
            f.close()

            self.assertEquals(contents, t)

        finally:
            # Cleanup.
            #
            # fixme: On Windows the file can't be removed!
            try:
                os.remove(tmp)

            except OSError:
                pass
            
        return

    # fixme: This test fails when port 1234 is already in use.
    def test_no_such_http_resource(self):
        """ no such http resource """
        
        httpd = HTTPServer(('localhost', 1234), SimpleHTTPRequestHandler)
        thread.start_new_thread(httpd.handle_request, ())

        # Open an HTTP document resource.
        rm = ResourceManager()

        self.failUnlessRaises(
            NoSuchResourceError, rm.file, 'http://localhost:1234/bogus.dat'
        )

        return

    def test_unknown_protocol(self):
        """ unknown protocol """

        # Open an HTTP document resource.
        rm = ResourceManager()

        self.failUnlessRaises(ValueError, rm.file, 'bogus://foo/bar/baz')
        
        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()
    
#### EOF ######################################################################
