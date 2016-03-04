""" Tests for the Enthought code browser. """

# Standard library imports.
import os.path
import logging

# Log to stidout (for now!).
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# Standard library imports.
import inspect, unittest

# Enthought library imports.
from traits.util.resource import get_path

from envisage.developer.code_browser.api import CodeBrowser



class CodeBrowserTestCase(unittest.TestCase):
    """ Tests for the Enthought code browser. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.code_browser = CodeBrowser()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return

    def assertIn(self, first, second, msg=None):
        # Python 2.6 compatibility layer.
        if hasattr(unittest.TestCase, 'assertIn'):
            unittest.TestCase.assertIn(self, first, second, msg)
        else:
            self.assertTrue(first in second, msg)

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_browse_this_module(self):
        """ browse this module """

        # We don't use '__file__' as the filename here as it could refer to the
        # '.pyc' file (we could just strip the 'c' of course, but inspect just
        # seems more intentional ;^).
        filename = inspect.getsourcefile(CodeBrowserTestCase)
        module = self.code_browser.read_file(filename)

        # Check the module name and documentation.
        self.assertTrue(module.name.endswith('code_browser_test_case'))
        self.assertEqual(" Tests for the Enthought code browser. ", module.doc)

        # Check that the module contains this class!
        klass = module.klasses['CodeBrowserTestCase']
        self.assertEqual(" Tests for the Enthought code browser. ", klass.doc)

        # And that the class contains this method.
        method = klass.methods['test_browse_this_module']
        self.assertEqual(" browse this module ", method.doc)

        return

    def test_has_traits(self):
        """ has traits """

        module = self.code_browser.read_file(
            os.path.join(get_path(CodeBrowserTestCase), 'example_1.py')
        )

        # Check the module name and documentation.
        self.assertTrue(module.name.endswith('example_1'))

        # Check that the module contains the specified class.
        klass = module.klasses.get('Base')
        self.assertNotEqual(None, klass)

        # Check the class' base class.
        self.assertEqual(['HasTraits'], klass.bases)

        # Check that the class has the appropriate traits and methods.
        self.assertEqual(2, len(klass.traits))
        self.assertIn("x", klass.traits)
        self.assertIn("y", klass.traits)

        self.assertEqual(2, len(klass.methods))
        self.assertIn("foo", klass.methods)
        self.assertIn("bar", klass.methods)

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
