# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the resource manager. """


# Standard library imports.
import unittest

from io import StringIO

# Major package imports.
from pkg_resources import resource_filename

# Enthought library imports.
from envisage.resource.api import ResourceManager
from envisage.resource.api import NoSuchResourceError
from envisage._compat import HTTPError, unicode_str
import envisage._compat
url_library = envisage._compat


# This module's package.
PKG = 'envisage.resource.tests'


# mimics `urlopen` for some tests.
# In setUp it replaces `urlopen` for some tests,
# and in tearDown, the regular `urlopen` is put back into place.
def stubout_urlopen(url):
    if 'bogus' in url:
        raise HTTPError(url, '404', 'No such resource', '', None)

    elif 'localhost' in url:
        return StringIO(unicode_str('This is a test file.\n'))

    else:
        raise ValueError('Unexpected URL %r in stubout_urlopen' % url)


class ResourceManagerTestCase(unittest.TestCase):
    """ Tests for the resource manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.stored_urlopen = url_library.urlopen
        url_library.urlopen = stubout_urlopen

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        url_library.urlopen = self.stored_urlopen

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_file_resource(self):
        """ file resource """

        rm = ResourceManager()

        # Get the filename of the 'api.py' file.
        filename = resource_filename('envisage.resource', 'api.py')

        # Open a file resource.
        f = rm.file('file://' + filename)
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()

        # Open the api file via the file system.
        with open(filename, 'rb') as g:
            self.assertEqual(g.read(), contents)

    def test_no_such_file_resource(self):
        """ no such file resource """

        rm = ResourceManager()

        # Open a file resource.
        with self.assertRaises(NoSuchResourceError):
            rm.file("file://../bogus.py")

    def test_package_resource(self):
        """ package resource """

        rm = ResourceManager()

        # Open a package resource.
        f = rm.file('pkgfile://envisage.resource/api.py')
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()

        # Get the filename of the 'api.py' file.
        filename = resource_filename('envisage.resource', 'api.py')

        # Open the api file via the file system.
        g = open(filename, 'rb')
        self.assertEqual(g.read(), contents)
        g.close()

    def test_no_such_package_resource(self):
        """ no such package resource """

        rm = ResourceManager()

        # Open a package resource.
        with self.assertRaises(NoSuchResourceError):
            rm.file("pkgfile://envisage.resource/bogus.py")

        with self.assertRaises(NoSuchResourceError):
            rm.file("pkgfile://completely.bogus/bogus.py")

    def test_http_resource(self):
        """ http resource """

        # Open an HTTP document resource.
        rm = ResourceManager()

        f = rm.file('http://localhost:1234/file.dat')
        self.assertNotEqual(f, None)
        contents = f.read()
        f.close()

        self.assertEqual(contents, 'This is a test file.\n')

    def test_no_such_http_resource(self):
        """ no such http resource """

        # Open an HTTP document resource.
        rm = ResourceManager()

        with self.assertRaises(NoSuchResourceError):
            rm.file("http://localhost:1234/bogus.dat")

    def test_unknown_protocol(self):
        """ unknown protocol """

        # Open an HTTP document resource.
        rm = ResourceManager()

        with self.assertRaises(ValueError):
            rm.file("bogus://foo/bar/baz")
