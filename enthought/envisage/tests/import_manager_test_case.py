""" Tests for the import manager. """


# Standard library imports.
import unittest

# Enthought library imports.
from enthought.envisage.api import ImportManager

# Local imports.
from event_tracker import EventTracker


class ImportManagerTestCase(unittest.TestCase):
    """ Tests for the import manager. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.import_manager = ImportManager()

        self.event_tracker  = EventTracker(
            subscriptions = [(self.import_manager, 'symbol_imported')]
        )

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_import_dotted_symbol(self):
        """ import dotted symbol """

        symbol = self.import_manager.import_symbol('unittest.TestCase')
        self.assertEqual(symbol, unittest.TestCase)

        # Make sure the right event was fired.
        self.assertEqual(1, len(self.event_tracker.events))
        obj, trait_name, old, new = self.event_tracker.events[0]
        self.assertEqual(trait_name, 'symbol_imported')
        self.assertEqual(new, unittest.TestCase)
        
        return

    def test_import_nested_symbol(self):
        """ import nested symbol """

        symbol = self.import_manager.import_symbol('unittest:TestCase.setUp')
        self.assertEqual(symbol, unittest.TestCase.setUp)

        # Make sure the right event was fired.
        self.assertEqual(1, len(self.event_tracker.events))
        obj, trait_name, old, new = self.event_tracker.events[0]
        self.assertEqual(trait_name, 'symbol_imported')
        self.assertEqual(new, unittest.TestCase.setUp)

        return

    def test_import_dotted_module(self):
        """ import dotted modulel """

        symbol = self.import_manager.import_symbol(
            'enthought.envisage3.api:ImportManager'
        )
        self.assertEqual(symbol, ImportManager)

        # Make sure the right event was fired.
        self.assertEqual(1, len(self.event_tracker.events))
        obj, trait_name, old, new = self.event_tracker.events[0]
        self.assertEqual(trait_name, 'symbol_imported')
        self.assertEqual(new, ImportManager)
        
        return

#### EOF ######################################################################
