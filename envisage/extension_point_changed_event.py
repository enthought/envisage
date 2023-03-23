# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An event fired when an extension point's extensions have changed. """


# Enthought library imports.
from traits.api import TraitListEvent


class ExtensionPointChangedEvent(TraitListEvent):
    """An event fired when an extension point's extensions have changed."""

    def __init__(self, extension_point_id=None, **kw):
        """Constructor."""

        # The base class has the 'index', 'removed' and 'added' attributes.
        super().__init__(**kw)

        # We add the extension point Id.
        self.extension_point_id = extension_point_id

    def __repr__(self):
        return (
            "ExtensionPointChangedEvent(extension_point_id={!r}, "
            "index={!r}, removed={!r}, added={!r})"
        ).format(self.extension_point_id, self.index, self.removed, self.added)
