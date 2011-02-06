# System library imports.
from scipy import arange, array
from scipy.integrate import odeint

# Enthought libary imports.
from enthought.traits.api import Adapter, Array, DelegatesTo, Float, \
     HasTraits, Instance, Property, Trait, Unicode, \
     adapts, cached_property, implements
from enthought.traits.ui.api import View, Item

# Local imports
from i_plottable_2d import IPlottable2D


class Rossler(HasTraits):
    """ The model object for the Rossler attractor.
    """

    # Equation parameters.
    a = Float(0.2, auto_set=False, enter_set=True)
    b = Float(0.2, auto_set=False, enter_set=True)
    c = Float(5.7, auto_set=False, enter_set=True)

    # Integration parameters.
    initial_point = Array(value=[0.0, 1.0, 0.0])
    time_start = Float(0.0)
    time_stop = Float(100.0)
    time_step = Float(0.01)
    time_points = Property(Array, depends_on='time_start, time_stop, time_step')

    # Integration results.
    data = Property(Array, depends_on=['a', 'b', 'c',
                                       'initial_point', 'time_points'])
    data_slice = Property(Array, depends_on='data, data_slice_dimension')
    data_slice_dimension = Trait('x', { 'x':0, 'y':1, 'z':2 })

    # Configuration view.
    view = View(Item('a'),
                Item('b'),
                Item('c'),
                Item('initial_point'),
                Item('time_start'),
                Item('time_stop'),
                Item('time_step'),
                resizable=True)

    def compute_step(self, point, time):
        x, y, z = point
        return array([ -y - z, x + self.a * y, self.b + z * (x - self.c) ])

    @cached_property
    def _get_data(self):
        return odeint(self.compute_step, self.initial_point, self.time_points)

    @cached_property
    def _get_data_slice(self):
        return self.data[:,self.data_slice_dimension_]

    @cached_property
    def _get_time_points(self):
        return arange(self.time_start, self.time_stop, self.time_step)


class RosslerIPlottable2DAdapter(Adapter):

    implements(IPlottable2D)
    
    adaptee = Instance(Rossler)

    x_data = DelegatesTo('adaptee', 'time_points')
    y_data = DelegatesTo('adaptee', 'data_slice')

    title = Unicode('Rossler Attractor')
    x_label = Unicode('time')
    y_label = DelegatesTo('adaptee', 'data_slice_dimension')

    view = View(Item('adaptee',
                     style='custom',
                     show_label=False))

adapts(RosslerIPlottable2DAdapter, Rossler, IPlottable2D)
