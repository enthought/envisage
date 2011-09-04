""" Lorenz example. """


# Major package imports.
from scipy import array, arange
from scipy.integrate import odeint

# Enthought library imports.
from chaco.chaco_plot_editor import ChacoPlotItem
from traits.api import Array, DelegatesTo, Float, HasTraits
from traits.api import Instance, List, Trait
from traitsui.api import Item, HGroup, VGroup, View


class Lorenz(HasTraits):
    """ The Lorenz model. """

    prandtl = Float(10.0, auto_set = False, enter_set = True)
    rayleigh = Float(28.0, auto_set = False, enter_set = True)
    beta = Float(8.0 / 3.0, auto_set = False, enter_set = True)
    # Give the dtype explicitly in the Array traits; this is a
    # work-around for trac ticket #1864.
    init = Array(value = array([0.0, 1.0, 0.0]), dtype=float)
    time = Array(value = array([0.0, 100.0, 0.01]), dtype=float)
    timePoints = Array()
    data3d = Array()
    output = Trait('x vs time', {'x vs time':0, 'y vs time':1, 'z vs time':2})
    data2d = Array()

    def refresh(self):
        self.calculatePoints()
        self.data2d=self.data3d[:,self.output_]

    def __init__(self): self.refresh()
    def _output_changed(self): self.refresh()
    def _prandtl_changed(self): self.refresh()
    def _rayleigh_changed(self): self.refresh()
    def _beta_changed(self): self.refresh()
    def _init_changed(self): self.refresh()
    def _time_changed(self): self.refresh()

    def lorenz(self, w, t, prandtl, rayleigh, beta):
        x, y, z = w
        return array([prandtl * (y - x), x*(rayleigh - z) - y, x*y - beta*z])

    def calculatePoints(self):
        init = self.init.copy()
        self.timePoints = arange(*self.time)
        self.data3d = odeint(
            self.lorenz, init, self.timePoints,
            args = (self.prandtl, self.rayleigh, self.beta)
        )

        return


class DataView(HasTraits):
    """ The data view. """

    # The model that we are a view of.
    lorenz = Instance(Lorenz)

    # The view traits.
    prandtl  = DelegatesTo('lorenz')
    rayleigh = DelegatesTo('lorenz')
    beta     = DelegatesTo('lorenz')
    init     = DelegatesTo('lorenz')
    time     = DelegatesTo('lorenz')

    traits_ui_view = View(
        Item('prandtl'),
        Item('rayleigh'),
        Item('beta'),
        Item('init'),
        Item('time'),
        id='lorenz.data',
        resizable=True
    )


class Plot2DView(HasTraits):
    """ The Plot 2D view. """

    # The model that we are a view of.
    lorenz = Instance(Lorenz)

    # The view traits.
    output     = DelegatesTo('lorenz')
    timePoints = DelegatesTo('lorenz')
    data2d     = DelegatesTo('lorenz')

    traits_ui_view = View(
        Item('output'),
        ChacoPlotItem(
            'timePoints', 'data2d',
            show_label       = False,
            resizable        = True,
            orientation      = 'h',
            title            = 'Plot',
            x_label          = 'time',
            y_label          = 'x',
            color            = 'red',
            bgcolor          = 'white',
            border_visible   = False ,
            border_width     = 1,
            padding_bg_color = 'lightgray'
        ),
        id        = 'lorenz.plot2d',
        resizable = True
    )

#### EOF ######################################################################
