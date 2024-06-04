# (C) Copyright 2007-2024 Enthought, Inc., Austin, TX
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


class FooPerspective(Perspective):
    """An example perspective."""

    # The perspective's name.
    name = "Foo"

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id="Blue", position="left"),
        PerspectiveItem(id="Red", position="with", relative_to="Blue"),
        PerspectiveItem(id="Green", position="top"),
    ]
