# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A view containing a yellow panel! """


# Local imports.
from .color_view import ColorView


class YellowView(ColorView):
    """A view containing a yellow panel!"""

    #### 'IView' interface ####################################################

    # The view's name.
    name = "Yellow"

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = "bottom"
