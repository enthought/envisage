# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the import manager. """

# Standard library imports.
import unittest

# Enthought library imports.
from envisage.api import Application, ImportManager


class ImportManagerTestCase(unittest.TestCase):
    """Tests for the import manager."""

    def setUp(self):
        """Prepares the test fixture before each test method is called."""

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.import_manager = Application(import_manager=ImportManager())

    def test_import_dotted_symbol(self):
        """import dotted symbol"""

        import tarfile

        symbol = self.import_manager.import_symbol("tarfile.TarFile")
        self.assertEqual(symbol, tarfile.TarFile)

    def test_import_nested_symbol(self):
        """import nested symbol"""

        import tarfile

        symbol = self.import_manager.import_symbol("tarfile:TarFile.open")
        self.assertEqual(symbol, tarfile.TarFile.open)

    def test_import_dotted_module(self):
        """import dotted module"""

        symbol = self.import_manager.import_symbol(
            "envisage.api:ImportManager"
        )
        self.assertEqual(symbol, ImportManager)
