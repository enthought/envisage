# System library imports.
from scipy import array, zeros

# Enthought library imports.
from traits.api import (
    Array,
    Float,
    HasTraits,
    Int,
    Property,
    Str,
    cached_property,
    provides,
)
from traitsui.api import Item, View

# Local imports.
from attractors.model.i_plottable_2d import IPlottable2d


@provides(IPlottable2d)
class Henon(HasTraits):
    """ The model object for the Henon map.
    """

    #### 'Henon' interface ####################################################

    # Equation parameters.
    a = Float(1.4, auto_set=False, enter_set=True)
    b = Float(0.3, auto_set=False, enter_set=True)

    # Iteration parameters.
    initial_point = Array(value=[0.1, 0.1])
    steps = Int(10000)

    # Iteration results.
    points = Property(Array, depends_on="a, b, initial_point, steps")

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
    x_data = Property(Array, depends_on="points")
    y_data = Property(Array, depends_on="points")
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
            point = array([y + 1 - self.a * x ** 2, self.b * x])
        return points

    @cached_property
    def _get_x_data(self):
        return self.points[:, 0]

    @cached_property
    def _get_y_data(self):
        return self.points[:, 1]
