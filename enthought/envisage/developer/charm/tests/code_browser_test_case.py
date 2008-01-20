""" Tests for the Enthought code browser. """


# Standard library imports.
import logging

# Create a log file.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# Standard library imports.
import os, random, shutil, unittest

# Enthought library imports.
from enthought.envisage.developer.charm.api import CodeBrowser


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
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_browse_this_module(self):
        """ browse this module """

        module = self.code_browser.read_file(__file__)

        # Check the module name and documentation.
        self.assertEqual('code_browser_test_case', module.name)
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

        module = self.code_browser.read_file('example_1.py')

        # Check the module name and documentation.
        self.assertEqual('example_1', module.name)

        # Check that the module contains the specified class.
        klass = module.klasses.get('Base')
        self.assertNotEqual(None, klass)

        # Check the class' base class.
        self.assertEqual(['HasTraits'], klass.bases)
        
        # Check that the class has the appropriate traits and methods.
        self.assertEqual(2, len(klass.traits))
        x = klass.traits['x']
        y = klass.traits['y']

        self.assertEqual(2, len(klass.methods))
        foo = klass.methods['foo']
        bar = klass.methods['bar']

        
        print x.lineno, y.lineno
        
        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
