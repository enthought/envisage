# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# Enthought library imports.
from traits.api import HasTraits, Str


class PreferencesCategory(HasTraits):
    """The description for a container of PreferencesPanes."""

    # The globally unique identifier for the category.
    id = Str

    # The user-visible name of the category.
    name = Str

    # The category appears after the category with this ID.
    before = Str

    # The category appears after the category with this ID.
    after = Str

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _name_default(self):
        """By default, use the ID for the name."""
        return self.id
