# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the base extension registry. """

# Standard library imports.
import unittest

# Enthought library imports.
from envisage.api import Application
from envisage.api import ExtensionRegistry

from envisage.extension_registry import ObservableExtensionRegistry
from envisage.tests.test_extension_registry_mixin import (
    ExtensionRegistryTestMixin,
    SettableExtensionRegistryTestMixin,
    ListeningExtensionRegistryTestMixin,
)


class ExtensionRegistryTestCase(
        ExtensionRegistryTestMixin,
        SettableExtensionRegistryTestMixin,
        ListeningExtensionRegistryTestMixin,
        unittest.TestCase,
):
    """ Tests for the base extension registry. """

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # We do all of the testing via the application to make sure it offers
        # the same interface!
        self.registry = Application(extension_registry=ExtensionRegistry())


class ObservableExtensionRegistryTestCase(
        ExtensionRegistryTestMixin,
        SettableExtensionRegistryTestMixin,
        ListeningExtensionRegistryTestMixin,
        unittest.TestCase,
):
    """ Tests for the base (?) observable extension registry. """

    def setUp(self):
        self.registry = ObservableExtensionRegistry()

    def test_nonmethod_listener_lifetime(self):
        with self.assertRaises(AssertionError):
            # Traits observe only holds a weak reference if the handler
            # is a method. In the case of a normal function, a strong
            # reference is held. But ExtensionPointRegistry holds a weak
            # reference regardless. Not sure if that is justified.
            super().test_nonmethod_listener_lifetime()
