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


class Lorenz(HasTraits):

    # Equation parameters.
    prandtl = Float(10.0, auto_set=False, enter_set=True)
    rayleigh = Float(28.0, auto_set=False, enter_set=True)
    beta = Float(8.0 / 3.0, auto_set=False, enter_set=True)

    # Integration parameters.
    initial_point = Array(value=[0.0, 1.0, 0.0])
    time_start = Float(0.0)
    time_stop = Float(100.0)
    time_step = Float(0.01)
    time_points = Property(Array, depends_on='time_start, time_stop, time_step')

    # Integration results.
    data = Property(Array, depends_on=['prandtl', 'rayleigh', 'beta',
                                       'initial_point', 'time_points'])
    data_slice = Property(Array, depends_on='data, data_slice_dimension')
    data_slice_dimension = Trait('x', { 'x':0, 'y':1, 'z':2 })

    # Configuration view.
    view = View(Item('prandtl'),
                Item('rayleigh'),
                Item('beta'),
                Item('initial_point'),
                Item('time_start'),
                Item('time_stop'),
                Item('time_step'),
                resizable=True)

    def compute_step(self, point, time):
        x, y, z = point
        return array([ self.prandtl * (y - x),
                       x * (self.rayleigh - z) - y,
                       x * y - self.beta * z ])

    @cached_property
    def _get_data(self):
        return odeint(self.compute_step, self.initial_point, self.time_points)

    @cached_property
    def _get_data_slice(self):
        return self.data[:,self.data_slice_dimension_]

    @cached_property
    def _get_time_points(self):
        return arange(self.time_start, self.time_stop, self.time_step)


class LorenzIPlottable2DAdapter(Adapter):

    implements(IPlottable2D)
    
    adaptee = Instance(Lorenz)

    x_data = DelegatesTo('adaptee', 'time_points')
    y_data = DelegatesTo('adaptee', 'data_slice')

    title = Unicode('Lorenz Attractor')
    x_label = Unicode('time')
    y_label = DelegatesTo('adaptee', 'data_slice_dimension')

adapts(LorenzIPlottable2DAdapter, Lorenz, IPlottable2D)
