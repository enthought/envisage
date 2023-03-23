# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The provider extension registry interface. """


# Local imports.
from .i_extension_registry import IExtensionRegistry


class IProviderExtensionRegistry(IExtensionRegistry):
    """The provider extension registry interface."""

    def add_provider(self, provider):
        """Add an extension provider."""

    def get_providers(self):
        """Return all of the providers in the registry."""

    def remove_provider(self, provider):
        """Remove an extension provider.

        Raise a 'ValueError' if the provider is not in the registry.

        """
