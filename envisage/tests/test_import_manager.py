""" Tests for the import manager. """


# Enthought library imports.
from envisage.api import Application, ImportManager
from traits.testing.unittest_tools import unittest


class ImportManagerTestCase(unittest.TestCase):
    """ Tests for the import manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.import_manager = Application(import_manager=ImportManager())

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return

    ###########################################################################
    # Tests.
    ###########################################################################

    def test_import_dotted_symbol(self):
        """ import dotted symbol """

        import tarfile

        symbol = self.import_manager.import_symbol('tarfile.TarFile')
        self.assertEqual(symbol, tarfile.TarFile)

        return

    def test_import_nested_symbol(self):
        """ import nested symbol """

        import tarfile

        symbol = self.import_manager.import_symbol('tarfile:TarFile.open')
        self.assertEqual(symbol, tarfile.TarFile.open)

        return

    def test_import_dotted_module(self):
        """ import dotted module """

        symbol = self.import_manager.import_symbol(
            'envisage.api:ImportManager'
        )
        self.assertEqual(symbol, ImportManager)

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
