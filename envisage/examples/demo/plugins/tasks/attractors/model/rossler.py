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

# Local imports
from attractors.model.i_model_3d import IModel3d, IModel3dIPlottable2dMixin
from attractors.model.i_plottable_2d import IPlottable2d
from scipy import arange, array
from scipy.integrate import odeint

# Enthought libary imports.
from traits.api import (
    Adapter,
    Array,
    cached_property,
    Float,
    HasTraits,
    Instance,
    Property,
    provides,
    register_factory,
    Str,
)
from traitsui.api import Item, View


@provides(IModel3d)
class Rossler(HasTraits):
    """The model object for the Rossler attractor."""

    #### 'IModel3d' interface #################################################

    name = Str("Rossler Attractor")
    points = Property(Array, observe="a, b, c, initial_point, times")

    #### 'Rossler' interface ##################################################

    # Equation parameters.
    a = Float(0.2, auto_set=False, enter_set=True)
    b = Float(0.2, auto_set=False, enter_set=True)
    c = Float(5.7, auto_set=False, enter_set=True)

    # Integration parameters.
    initial_point = Array(dtype=np.float64, value=[0.0, 1.0, 0.0])
    time_start = Float(0.0)
    time_stop = Float(100.0)
    time_step = Float(0.01)
    times = Property(Array, observe="time_start, time_stop, time_step")

    # Configuration view.
    view = View(
        Item("a"),
        Item("b"),
        Item("c"),
        Item("initial_point"),
        Item("time_start"),
        Item("time_stop"),
        Item("time_step"),
        resizable=True,
    )

    ###########################################################################
    # 'Rossler' interface.
    ###########################################################################

    def compute_step(self, point, time):
        x, y, z = point
        return array([-y - z, x + self.a * y, self.b + z * (x - self.c)])

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @cached_property
    def _get_points(self):
        return odeint(self.compute_step, self.initial_point, self.times)

    @cached_property
    def _get_times(self):
        return arange(self.time_start, self.time_stop, self.time_step)


@provides(IPlottable2d)
class RosslerIPlottable2dAdapter(Adapter, IModel3dIPlottable2dMixin):
    adaptee = Instance(Rossler)

    plot_type = Str("line")


register_factory(RosslerIPlottable2dAdapter, Rossler, IPlottable2d)
