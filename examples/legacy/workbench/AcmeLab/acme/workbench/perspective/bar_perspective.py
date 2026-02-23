# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" An example perspective. """


# Enthought library imports.
from pyface.workbench.api import Perspective, PerspectiveItem


class BarPerspective(Perspective):
    """An example perspective."""

    # The perspective's name.
    name = "Bar"

    # Should the editor area be shown in this perspective?
    show_editor_area = False

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id="Green"),
        PerspectiveItem(id="Black", position="bottom", relative_to="Green"),
    ]
