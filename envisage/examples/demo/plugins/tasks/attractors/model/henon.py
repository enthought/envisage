# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# System library imports.
import numpy as np

# Local imports.
from attractors.model.i_plottable_2d import IPlottable2d
from scipy import array, zeros

# Enthought library imports.
from traits.api import (
    Array,
    cached_property,
    Float,
    HasTraits,
    Int,
    Property,
    provides,
    Str,
)
from traitsui.api import Item, View


@provides(IPlottable2d)
class Henon(HasTraits):
    """The model object for the Henon map."""

    #### 'Henon' interface ####################################################

    # Equation parameters.
    a = Float(1.4, auto_set=False, enter_set=True)
    b = Float(0.3, auto_set=False, enter_set=True)

    # Iteration parameters.
    initial_point = Array(dtype=np.float64, value=[0.1, 0.1])
    steps = Int(10000)

    # Iteration results.
    points = Property(Array, observe="a, b, initial_point, steps")

    # Configuration view.
    view = View(
        Item("a"),
        Item("b"),
        Item("initial_point"),
        Item("steps"),
        resizable=True,
    )

    #### 'IPlottable2D' interface #############################################

    name = Str("Henon Map")
    plot_type = Str("scatter")
    x_data = Property(Array, observe="points")
    y_data = Property(Array, observe="points")
    x_label = Str("x")
    y_label = Str("y")

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @cached_property
    def _get_points(self):
        point = self.initial_point
        points = zeros((self.steps, 2))
        for i in range(self.steps):
            x, y = points[i] = point
            point = array([y + 1 - self.a * x**2, self.b * x])
        return points

    @cached_property
    def _get_x_data(self):
        return self.points[:, 0]

    @cached_property
    def _get_y_data(self):
        return self.points[:, 1]
