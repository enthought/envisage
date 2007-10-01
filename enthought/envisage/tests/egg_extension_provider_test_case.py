""" Tests for the Egg extension registry. """


# Enthought library imports.
from enthought.envisage.api import EggExtensionProvider, ExtensionPoint
from enthought.envisage.api import ExtensionRegistry
from enthought.traits.api import Dict

# Local imports.
from egg_based_test_case import EggBasedTestCase


class EggExtensionRegistryTestCase(EggBasedTestCase):
    """ Tests for the Egg extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        EggBasedTestCase.setUp(self)

        # Create a new extension registry.
        ExtensionPoint.extension_registry = ExtensionRegistry(
            providers=[EggExtensionProvider()]
        )
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_egg_extension_provider(self):
        """ egg extension provider """

        self._add_egg('acme.motd-0.1a1-py2.4.egg')
        self._add_egg('acme.motd.software_quotes-0.1a1-py2.4.egg')

        # Acme library imports.
        from acme.motd.api import Message, ExtensibleMOTD
        from acme.motd.software_quotes import messages

        # Get the message of the day...
        motd    = ExtensibleMOTD()
        message = motd.motd()

        # ... and print it.
        print '\n"%s"\n\n- %s' % (message.text, message.author)

        # Make sure it was one of the contributed ones!
        self.assertNotEqual(None, message)
        self.assertEqual(Message, type(message))
        self.assertNotEqual(None, self._find_object(message, messages))

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _find_object(self, obj, namespace):
        """ Look for an object in a namespace.

        Return None if no such object exists.

        """

        for name, value in namespace.__dict__.items():
            if obj is value:
                break

        else:
            obj = None

        return obj

#### EOF ######################################################################
