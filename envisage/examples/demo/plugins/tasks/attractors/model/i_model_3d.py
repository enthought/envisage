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
from traits.api import (
    Array,
    cached_property,
    DelegatesTo,
    HasTraits,
    Instance,
    Interface,
    Property,
    Str,
    Trait,
)
from traitsui.api import Group, Item, View


class IModel3d(Interface):
    """A model object that produces an array of 3D points."""

    # The user-visible name of the model.
    name = Str

    # An n-by-3 array.
    points = Array


class IModel3dIPlottable2dMixin(HasTraits):
    """
    Mixin class to facilitate defining a IModel3d -> IPlottable2D adapter.
    """

    #### 'Adapter' interface ##################################################

    adaptee = Instance(IModel3d)

    #### 'IPlottable2D' interface #############################################

    name = DelegatesTo("adaptee")

    x_data = Property(Array, observe="adaptee.points, x_label")
    y_data = Property(Array, observe="adaptee.points, y_label")

    x_label = Trait("x", {"x": 0, "y": 1, "z": 2})
    y_label = Trait("y", {"x": 0, "y": 1, "z": 2})

    view = View(
        Group(
            Group(
                Item("adaptee", style="custom", show_label=False),
                label="Model",
            ),
            Group(
                Item("x_label", label="X axis"),
                Item("y_label", label="Y axis"),
                label="Plot",
            ),
        )
    )

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @cached_property
    def _get_x_data(self):
        return self.adaptee.points[:, self.x_label_]

    @cached_property
    def _get_y_data(self):
        return self.adaptee.points[:, self.y_label_]
