# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" Tests for the 'Service' trait type. """


# Enthought library imports.
from envisage.api import Application, Plugin, Service
from traits.api import HasTraits, Instance
from traits.testing.unittest_tools import unittest


class TestApplication(Application):
    """ The type of application used in the tests. """

    id = 'test'


class ServiceTestCase(unittest.TestCase):
    """ Tests for the 'Service' trait type. """

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

    def test_service_trait_type(self):
        """ service trait type"""

        class Foo(HasTraits):
            pass

        class PluginA(Plugin):
            id = 'A'
            foo = Instance(Foo, (), service=True)

        class PluginB(Plugin):
            id = 'B'
            foo = Service(Foo)

        a = PluginA()
        b = PluginB()

        application = TestApplication(plugins=[a, b])
        application.start()

        # Make sure the services were registered.
        self.assertEqual(a.foo, b.foo)

        # Stop the application.
        application.stop()

        # Make sure the service was unregistered.
        self.assertEqual(None, b.foo)

        # You can't set service traits!
        self.failUnlessRaises(SystemError, setattr, b, 'foo', 'bogus')

        return

    def test_service_trait_type_with_no_service_registry(self):
        """ service trait type with no service registry """

        class Foo(HasTraits):
            pass

        class Bar(HasTraits):
            foo = Service(Foo)

        # We should get an exception because the object does not have an
        # 'service_registry' trait.
        b = Bar()
        self.failUnlessRaises(ValueError, getattr, b, 'foo')

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
